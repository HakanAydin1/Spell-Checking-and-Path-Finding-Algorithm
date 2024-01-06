import time
import matplotlib.pyplot as plt
import collections
from collections import deque
import bisect
import re


def build_word_list_linear(filename):
    with open(filename, 'r') as file:
        return [word.strip().lower() for word in file]


def spell_check_linear_list(text, word_list):
    return [word for word in text if word.lower() not in word_list]


def build_word_list_bbst(filename):
    word_list = []
    with open(filename, 'r') as file:
        for word in file:
            word = word.strip().lower()
            bisect.insort_left(word_list, word)
    return word_list


def spell_check_bbst(text, word_list):
    return [word for word in text if bisect.bisect_left(word_list, word.lower()) == len(word_list) or word_list[bisect.bisect_left(word_list, word.lower())] != word.lower()]


class TrieNode:
    def __init__(self):
        self.children = collections.defaultdict(TrieNode)
        self.is_word = False


def build_word_list_trie(filename):
    root = TrieNode()
    with open(filename, 'r') as file:
        for word in file:
            word = word.strip().lower()
            current = root
            for char in word:
                current = current.children[char]
            current.is_word = True
    return root


def spell_check_trie(text, trie):
    def dfs(node, prefix):
        if node.is_word:
            return []
        misspelled_words = []
        for char in node.children:
            misspelled_words.extend(dfs(node.children[char], prefix + char))
        return misspelled_words

    misspelled_words = []
    for word in text:
        current = trie
        for char in word:
            if char in current.children:
                current = current.children[char]
            else:
                misspelled_words.append(word)
                break
    return misspelled_words


def build_word_list_hash_map(filename):
    word_set = set()
    with open(filename, 'r') as file:
        for word in file:
            word_set.add(word.strip().lower())
    return word_set


def spell_check_hash_map(text, word_set):
    return [word for word in text if word.lower() not in word_set]


def measure_time(build_func, check_func, text_length):
    start_time = time.time()
    word_list = build_func('wordlist.txt')
    dictionary_build_time = time.time() - start_time

    text = ['word'] * text_length

    start_time = time.time()
    misspelled_words = check_func(text, word_list)
    spell_check_time = time.time() - start_time

    return dictionary_build_time, spell_check_time


def spell_check_text_file(text_file, word_list):
    misspelled_words = []
    with open(text_file, 'r') as file:
        for line in file:
            words = re.findall(r'\b\w+\b', line)
            for word in words:
                if word.lower() not in word_list:
                    misspelled_words.append(word)
    return misspelled_words


# Measure running times for different approaches and text lengths
text_lengths = list(range(1000, 10001, 1000))
linear_list_build_times = []
linear_list_spell_check_times = []
bbst_build_times = []
bbst_spell_check_times = []
trie_build_times = []
trie_spell_check_times = []
hash_map_build_times = []
hash_map_spell_check_times = []

for length in text_lengths:
    linear_list_build_time, linear_list_spell_check_time = measure_time(build_word_list_linear, spell_check_linear_list, length)
    linear_list_build_times.append(linear_list_build_time)
    linear_list_spell_check_times.append(linear_list_spell_check_time)

    bbst_build_time, bbst_spell_check_time = measure_time(build_word_list_bbst, spell_check_bbst, length)
    bbst_build_times.append(bbst_build_time)
    bbst_spell_check_times.append(bbst_spell_check_time)

    trie_build_time, trie_spell_check_time = measure_time(build_word_list_trie, spell_check_trie, length)
    trie_build_times.append(trie_build_time)
    trie_spell_check_times.append(trie_spell_check_time)

    hash_map_build_time, hash_map_spell_check_time = measure_time(build_word_list_hash_map, spell_check_hash_map, length)
    hash_map_build_times.append(hash_map_build_time)
    hash_map_spell_check_times.append(hash_map_spell_check_time)

# Generate graphs
plt.plot(text_lengths, linear_list_build_times, label='Linear List')
plt.plot(text_lengths, bbst_build_times, label='BBST')
plt.plot(text_lengths, trie_build_times, label='Trie')
plt.plot(text_lengths, hash_map_build_times, label='Hash Map')
plt.xlabel('Text Length')
plt.ylabel('Running Time (seconds)')
plt.title('Dictionary Building Time vs. Text Length')
plt.legend()
plt.show()

plt.plot(text_lengths, linear_list_spell_check_times, label='Linear List')
plt.plot(text_lengths, bbst_spell_check_times, label='BBST')
plt.plot(text_lengths, trie_spell_check_times, label='Trie')
plt.plot(text_lengths, hash_map_spell_check_times, label='Hash Map')
plt.xlabel('Text Length')
plt.ylabel('Running Time (seconds)')
plt.title('Spell Checking Time vs. Text Length')
plt.legend()
plt.show()

# Spell check example text file
text_file = 'example_text.txt'
word_list = build_word_list_linear('wordlist.txt')
misspelled_words = spell_check_text_file(text_file, word_list)
print("Misspelled words:", misspelled_words)

def find_shortest_path(labyrinth, start, speeds, end):
    rows = len(labyrinth)
    cols = len(labyrinth[0])
    visited = [[False] * cols for _ in range(rows)]
    queue = deque([(start, 0)])
    visited[start[0]][start[1]] = True

    while queue:
        current, distance = queue.popleft()

        if current == end:
            return distance / speeds[current]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy

            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and labyrinth[nx][ny] != '#':
                queue.append(((nx, ny), distance + 1))
                visited[nx][ny] = True

    return -1

# Example usage
labyrinth = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', 'S', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', ' ', '#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', '#', '#', '#', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', 'E', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
]

# Example wizard positions and speeds
wizard_positions = [(1, 1), (2, 1), (1, 2)]  # Modify with the actual positions
wizard_speeds = [2, 3, 1]  # Modify with the actual speeds
exit_position = (9, 7)  # Modify with the actual exit position

shortest_paths = []
for position in wizard_positions:
    shortest_path = find_shortest_path(labyrinth, position, wizard_speeds, exit_position)
    shortest_paths.append(shortest_path)

fastest_wizard_index = shortest_paths.index(min(shortest_paths))
fastest_wizard_position = wizard_positions[fastest_wizard_index]
fastest_wizard_speed = wizard_speeds[fastest_wizard_index]

print(f"The wizard at position {fastest_wizard_position} with speed {fastest_wizard_speed} will reach the exit first.")
