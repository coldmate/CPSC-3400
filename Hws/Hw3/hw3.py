def marked():
    firstLine = False
    blocks = 0
    marked = set()
    
    for line in open("sample.txt"):
        if not firstLine:
            blocks = int(line)
            firstLine = True
            continue
        
        x, y = line.strip().split(',')

        if x.isalpha() and y.isdigit(): 
            marked.add(int(y))
        elif x.isdigit() and int(x) in marked:            
            marked.add(int(y))           

    return blocks, marked

    
def _main():

    blocks, marked_nodes = marked()

    all_nodes = set(range(blocks))
    swept_nodes = all_nodes - marked_nodes

    print("Marked nodes:", " ".join(map(str, sorted(marked_nodes))))
    print("Swept nodes:", " ".join(map(str, sorted(swept_nodes))))

if __name__ == "__main__":
    _main()

