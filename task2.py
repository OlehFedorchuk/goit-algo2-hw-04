from trie import Trie


class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        """
        Повертає кількість слів у Trie, які закінчуються на заданий суфікс pattern.
        Враховує регістр символів.
        """

        if not isinstance(pattern, str):
            raise TypeError("Pattern має бути рядком")

        count = 0

        def dfs(node, current_word):
            nonlocal count

            # Якщо у вузлі є value, значить це кінець слова
            if hasattr(node, "value") and node.value is not None:
                if current_word.endswith(pattern):
                    count += 1

            # Рекурсивно проходимо по всіх дочірніх вузлах
            for char, child_node in node.children.items():
                dfs(child_node, current_word + char)

        dfs(self.root, "")

        return count

    def has_prefix(self, prefix) -> bool:
        """
        Перевіряє, чи існує хоча б одне слово у Trie із заданим префіксом.
        Враховує регістр символів.
        """

        if not isinstance(prefix, str):
            raise TypeError("Prefix має бути рядком")

        node = self.root

        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]

        return True


if __name__ == "__main__":
    trie = Homework()

    words = ["apple", "application", "banana", "cat"]

    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1       # apple
    assert trie.count_words_with_suffix("ion") == 1     # application
    assert trie.count_words_with_suffix("a") == 1       # banana
    assert trie.count_words_with_suffix("at") == 1      # cat
    assert trie.count_words_with_suffix("xyz") == 0

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True               # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True               # banana
    assert trie.has_prefix("ca") == True                # cat

    # Перевірка регістру
    assert trie.has_prefix("App") == False
    assert trie.count_words_with_suffix("E") == 0

    print("Усі тести пройдено успішно!")