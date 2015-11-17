import os
print [name for name in os.listdir(".") if os.path.isdir(name)]