from collections import defaultdict

# Free-to-play grid dimensions
grid_size = 4
board = [[''] * grid_size] * grid_size
output = []

# Traversing through every single combination of letters is inefficient, especially if some traversals lead to dead ends anyways. 
# Therefore, we can implement a trie to check if the current node in the trie has any children. If not, there are no more possible words, so we continue our search on another node. 

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.full_word = False

root = TrieNode()

def make_trie():
    with open('./clean_wordbank.txt', 'r') as bank:
        for word in bank:
            curr = root
            word = word.strip()
            for letter in word:
                if letter not in curr.children:
                    curr.children[letter] = TrieNode()
                curr = curr.children[letter]
            curr.full_word = True

# DFS function to try every valid combination of letters.
def dfs(r, c, word, visited, node):
    if r < 0 or r >= grid_size or c < 0 or c >= grid_size:
        return
    if visited[r][c]:
        return
    
    letter = board[r][c]

    if letter not in node.children:
        return
    
    word += letter
    visited[r][c] = True

    if len(word) >= 3 and node.children[letter].full_word:
        output.append(word)

    directions = [
                (-1, 0), (-1, 1), 
                (0, 1), (1, 1), 
                (1, 0), (1, -1), 
                (0, -1),(-1, -1)]
    
    for x, y in directions:
        if 0 <= r + x < 4 and 0 <= c + y < 4 and not visited[r + x][c + y]:
            dfs(r + x, c + y, word, visited, node.children[letter])
    
    visited[r][c] = False

def calculate_points(word_length):
    point_system = {
        3: 100,
        4: 400,
        5: 800,
        6: 1400,
        7: 1800,
        8: 2200,
        9: 2600,
        10: 3000,
        11: 3400,
        12: 3800,
        13: 4200,
        14: 4600,
        15: 5000,
        16: 5400
    }
    return point_system.get(word_length, 0)

def main():
    make_trie()
    read = input("Enter letters left to right, top to bottom: ")

    board[0] = read[:4].upper()
    board[1] = read[4:8].upper()
    board[2] = read[8:12].upper()
    board[3] = read[12:16].upper()

    print(board)

    visited = [[False] * grid_size for _ in range(grid_size)]

    for i in range(grid_size):
        for j in range(grid_size):
            dfs(i, j, "", visited, root)
    
    output.sort(key=lambda x: calculate_points(len(x)), reverse=True)
    print(f"Words Generated: {len(output)}")
    print(f"Highest Possible Score: {sum(calculate_points(len(word)) for word in output)}")

    for word in output:
        print(f"{word} (Points: {calculate_points(len(word))})")

if __name__ == "__main__":
    main()