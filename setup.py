from sys import path as paths

additions = [
    r"[yourpath]\Simple-Bioenergy-Comparison-Model",
    r"[yourpath]\Simple-Bioenergy-Comparison-Model\Core_Model",
]


for i in additions:
    if i not in paths:
        paths.append(i)
        print(f"Added {i} to paths")
