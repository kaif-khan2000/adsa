
def preorder(roots,i,j,strings):
    if i>j:
        return
    # print the root
    print(strings[roots[i][j]],end=" ")
    #traverse left subtree
    preorder(roots,i,roots[i][j]-1,strings)
    # traverse right subtree
    preorder(roots,roots[i][j]+1,j,strings)

def obst(n,strings,prob):
    # create a 2D array to store the results
    # cost[i][j] stores the cost of the optimal binary search tree for keys i to j
    cost = [[0 for i in range(n)] for j in range(n)]
    # roots[i][j] stores the root of the optimal binary search tree for keys i to j
    roots = [[0 for i in range(n)] for j in range(n)]

    # initialize the cost matrix with diagonal elements
    for i in range(n):
        cost[i][i] = prob[i]
        roots[i][i] = i

    # fill the cost matrix
    # for each iteration of i we have to decide the space between i and j 
    # for 1st iteration size = 1 , (i,j) = (0,1),(1,2),(2,3)... )
    # for 2nd iteration size = 2 , (i,j) = (0,2),(1,3),(2,4)... )
    # and so on
    #  
    for size in range(2,n+1):
        for i in range(n-size+2):
            j = i + size - 1
            # if j exceeds the limit then break
            if(j>=n):
                break
            # if i exceeds the limit then break
            if(i>=n):
                break

            # initialize the cost with the maximum value
            cost[i][j] = 999999

            # now for selecting the root at each level using dynamic programming
            # cost[i][j] = min(cost[i][k-1] + cost[k+1][j] + sum(prob[i:j+1])) for k = i to j
            for root in range(i,j+1):
                temp = 0
                if(root>i):
                    temp += cost[i][root-1]
                if(root<j):
                    temp += cost[root+1][j]
                temp += sum(prob[i:j+1])
                if temp < cost[i][j]:
                    cost[i][j] = temp
                    # and also store the root
                    roots[i][j] = root
    # return the result
    return cost[0][n-1],roots
            
            



def main():
    strings = []
    prob = []
    # read the input from the user
    
    n = int(input("How many strings do you want to insert in the BST? "))
    print("Enter",n,"strings in sorted dictionary order along with their probabilities:")
    for i in range(n):
        string = input()
        strings.append(string)
        prob.append(float(input()))

    # n = 7
    # strings = ['a','am','and','egg','if','the','two']
    # prob = [0.22,0.18,0.2,0.05,0.25,0.02,0.08]



    flag = False
    # check weather the strings in dictionary order or not
    for i in range(n-1):
        if strings[i] > strings[i+1]:
            print("Strings are not in dictionary order.",end="")
            flag = True
    
    # check if the probabilities are distinct or not
    lis = list(set(prob))
    if len(lis) != len(prob):
        print("Probabilities are not distinct.",end="")
        flag = True

    # check the probabilities add upto 1 or not
    if round(sum(prob),4) != 1:
        print("Probabilities do not add upto 1.")
        flag = True

    if flag:
        print()
        return

    # call the function to calculate the cost of the optimal binary search tree
    res,roots = obst(n,strings,prob)
    # print the result
    print("The optimal binary search tree is:", res)
    # print the preorder traversal of the optimal binary search tree
    preorder(roots,0,n-1,strings)
    print()
    

if __name__ == "__main__":
    main()
