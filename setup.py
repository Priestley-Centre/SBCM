from sys import path as paths

additions = [
    r"Z:\Git\Simple-Bioenergy-Comparison-Model",
    r"Z:\Git\Simple-Bioenergy-Comparison-Model\Core_Model",
    r"Z:\Git\Simple-Bioenergy-Comparison-Model\Model_Runs",
    r"C:\Git Archive\Simple-Bioenergy-Comparison-Model",
    r"C:\Git Archive\Simple-Bioenergy-Comparison-Model\Core_Model",
    r"C:\Git Archive\Simple-Bioenergy-Comparison-Model\Model_Runs",
]


for i in additions:
    if i not in paths:
        paths.append(i)
        print(f"Added {i} to paths")
