from math import cos,sin,pi

roots = []

#printing a polynomial
def print_poly(deg,poly):
    for i in range(deg,-1,-1):

        # if coefficient is 0, skip
        if(poly[i] == 0):
            continue
        
        # if coefficient is 1 or -1, print x^i
        if((poly[i] == 1 or poly[i] == -1)):
            x = poly[i]
            if(i == deg and x>0):
                print("x*{} ".format(i),end="")
            elif(i == 0 and x>0):
                print("{} ".format(x),end="")
            elif(i == 0 and x<0):
                print("- {} ".format(-x),end="")
            elif(x < 0):
                print(" - x*{} ".format(i),end="")
            else:
                print(" + x*{} ".format(i),end="")
            continue
        
        
        else:
            x = poly[i]

        # if power is 0, print the coefficient
        if i == 0:
            if(poly[i]<0):
                print(" -",abs(poly[i]),"")
            else:
                print(" +",poly[i],"")
        # if power is is the highest power, print the coefficient and yx^i
        elif i == deg:
            print("{}x*{}".format(x,i),end="")
        else:
            if(x < 0):
                print(" - {}x*{} ".format(abs(x),i),end="")
            else:
                print(" + {}x*{} ".format(x,i),end="")
    print()

#reading a polynomial from user
def read_poly(n):
    deg_1 = int(input("Enter the degree of "+n+" polynomial: "))
    poly_1 = input("Enter the "+str(deg_1+1)+" coefficients of the "+n+" polynomial in the increasing order of the degree of the monomials they belong to:\n").split(" ")
    poly_1 = [int(i) for i in poly_1]

    return deg_1,poly_1

#naive multiplication
def naive_polynomial_multiplication(deg_1,poly_1,deg_2,poly_2):
    deg_3 = deg_1 + deg_2
    poly_3 = [0]*(deg_3+1)
    for i in range(deg_1+1):
        for j in range(deg_2+1):
            poly_3[i+j] += poly_1[i]*poly_2[j]
    return deg_3,poly_3

#add to complex numbers
def add_complex_num(a,b,c,d):
    return a+c,b+d

#multiply two complex numbers
def multiply_complex_num(a,b,c,d):
    return a*c-b*d,a*d+b*c

# smallest power of 2 greater than or equal to n
def find_N(deg_1,deg_2):
    n = deg_1+deg_2+1
    p = 1
    if (n and not(n & (n - 1))):
        return n
    while (p < n):
        p <<= 1
    return p

# find compex roots of unity
def find_complex_roots(n):
    for i in range(n):
        roots.append([cos(2*pi*i/n),sin(2*pi*i/n)])



# eval polynomial at a points
def Eval(poly,N,val=1):

    # if not in complex number format, convert to complex number format
    if val == 0:
        for i in range(N):
            poly[i] = [poly[i],0]
        #print("check",poly)

    # if N is 1 then return poly
    if N == 1:
        return [[poly[0][0],poly[0][1]]]

    # find the even and odd terms
    A0 = []
    A1 = []
    for i in range(N):
        if i%2 == 0:
            A0.append(poly[i])
        else:
            A1.append(poly[i])
    
    # evaluate the even and odd terms
    A0res = Eval(A0,N//2,1)
    A1res = Eval(A1,N//2,1)
    res = []
    for i in range(N):
        res.append([0,0])

    # mathematical formula for evaluation    
    root = [1,0]
    rootn = [cos(2*pi/N),sin(2*pi/N)]
    for i in range(N//2):
        mul0,mul1 = multiply_complex_num(root[0],root[1],A1res[i][0],A1res[i][1])
        res[i][0],res[i][1] = add_complex_num(A0res[i][0],A0res[i][1],mul0,mul1)
        res[i+N//2][0],res[i+N//2][1] = add_complex_num(A0res[i][0],A0res[i][1],-mul0,-mul1)
        root[0],root[1] = multiply_complex_num(root[0],root[1],rootn[0],rootn[1])
    return res

# product of 2 polynomial evaluations
def product_polynomial_evaluations(eval1,eval2,N):
    temp = []
    for i in range(N):
        # apply product on complex numbers i.e multiply two point forms
        prod0,prod1 = multiply_complex_num(eval1[i][0],eval1[i][1],eval2[i][0],eval2[i][1])
        temp.append([prod0,prod1])
    
    return temp


def iEval(poly,N):
    y = []
    # get the conjugate of the polynomial evaluation
    for i in range(N):
        y.append([poly[i][0],-poly[i][1]])
    # evaluate the conjugate polynomial
    y = Eval(y,N,1)
    # get the conjugate of the evaluation
    for i in range(N):
        y[i] = [y[i][0],-y[i][1]]

    # divide by N
    for i in range(N):
        y[i][0] = round(y[i][0]/N)
        y[i][1] = round(y[i][1]/N)
    return y

#main function
def main():
    # reading 2 polynomials
    deg_1,poly_1 = read_poly("first")
    deg_2,poly_2 = read_poly("second")
    # deg_1, poly_1 = 4, [-1,0,3,2,1]
    # deg_2, poly_2 = 3, [1,0,5,4]
    
    #printing those 2 polynomials in readable format.
    print("The first polynomial is: ")
    print_poly(deg_1,poly_1)
    print("The second polynomial is: ")
    print_poly(deg_2,poly_2)

    # applying naive multiplication
    res_deg,res_poly = naive_polynomial_multiplication(deg_1,poly_1,deg_2,poly_2)
    
    #printing the result of naive multiplication
    print("The product of the two polynomials obtained via naive polynomial multiplication is:")
    print_poly(res_deg,res_poly)

    # finding the smallest power of 2 greater than or equal to the degree of the product of the 2 polynomials
    N = find_N(deg_1,deg_2)

    # finding the complex roots of unity
    find_complex_roots(N)
    # print(roots)
    
    # append extra zeros to the polynomials
    poly_1_temp = poly_1 + [0]*(N-deg_1-1)
    poly_2_temp = poly_2 + [0]*(N-deg_2-1)

    #apply eval on the polynomials
    poly_1_evaluations = Eval(poly_1_temp,N,0)
    poly_2_evaluations = Eval(poly_2_temp,N,0)

    # product the point value forms of the 2 polynomials
    product_poly_evaluations = product_polynomial_evaluations(poly_1_evaluations,poly_2_evaluations,N)

    #now apply iEval on the product of the 2 polynomials
    inv = iEval(product_poly_evaluations,N)
    
    # get the coefficients of the product polynomial
    values = []
    for i in range(N):
        values.append(inv[i][0])
    #print(values)
    #printing the result of FFT multiplication
    print("The product of the two polynomials obtained via polynomial multiplication using FFT is:")
    print_poly(deg_1+deg_2,values)
    
if __name__ == "__main__":
    main()
    