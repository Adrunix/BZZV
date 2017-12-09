# Importation of Libaries 
from sympy.matrices import Matrix, eye, zeros, ones, diag, GramSchmidt # Imports matrix functions from sympy.
from sympy import poly # Imports polynomial functions from sympy,
from sympy import * # Imports the usage of x, y, and z as symbolic variables for algebraic maniplation.
x, y, z = symbols('x,y,z')
from sympy.plotting import plot3d
from sympy import symbols

GPS_DATA = Matrix([[25.767368,-80.18930],[34.088808,-118.40612],[40.727093,-73.97864]]);

def Numerator(GPS_DATA): # Defines the function that generates the numerator of the Lagrange interpolation Equation.
    # Defining of Variables
    Independent_Variable = GPS_DATA[:,0] # This pulls the first colunm of the inputted GPS data.
    Numerator_Total = zeros(1,len(Independent_Variable)) # This initializes a matrix filled with zeros for later storage.
    Numerator = [] # This initializes an empty list for later storage.
    Numerator_List = []  # This initializes an empty list for later storage.
    # Generation 
    for i in range(len(Independent_Variable)): # This generates all possible elements that make up the components of the numerator.
        Numerator_Total[i] = (x -  Independent_Variable[i])# This for loop takes the differences of x - i, where i is each element of independent variable colunm matrix.
    # Refinment    
    for i in range(len(Independent_Variable)): # This takes out (x - i) form the components of the numerator (Numerator_Total) and put the rest of terms in a list of matrices.
        Numerator_List.append(Numerator_Total[:i]+Numerator_Total[(i+1):]) # This goes through through the matrix and takes all the terms up to i, then all the terms after i, and puts them in a list.  
    # Multiplication    
    for i in Numerator_List : # Multplies the terms in the list of matrices together so there is only a list of polynomials.
        b = 1 # initial value of b that does not effect the value of t.
        for t in i: # This takes terms at index i in the list multplies them. 
            t,b = b,t * b
        Numerator.append(poly(b)) # This converts each polynomial from the previous for loop into polynomial "object" so sympy libary can perform algebraic maniplation and simplication of the generated expression.    
    return Numerator # Returns numerator terms from the function when Numerator function executes.
   
def Denominator(GPS_DATA): # Defines the function that generates the denominator of the Lagrange interpolation Equation.
    # Defining of Variables
    Independent_Variable =  GPS_DATA[:,0] #This pulls the first colunm of the inputted GPS data.
    Denominator = [] # This initializes an empty list for later storage.
    Denominator_Not_Multiplied = [] # This initializes an empty list for later storage.
    # Generation and Refinement
    for i in Independent_Variable: # This takes all the terms from independent variable and takes the differences of all the terms with each other. 
        Denominator_Total = [] # This initializes an empty list for later storage that is erased at the end of each loop. 
        for x in Independent_Variable: #
            if (i - x) != 0: # If the term does not zero it gets append to the list.
                Denominator_Total.append(i - x) # This appends the difference of i and x.
            else: # Else the for loop ends its current iteration and moves the next one. 
                continue
        Denominator_Not_Multiplied.append(Denominator_Total)# Takes the list from the inner for loop and puts it into another list, creating a list of list, before it is deleted by the next iteration of the outer for loop.
    # Multiplication    
    for i in  Denominator_Not_Multiplied: # Multplies the terms in the list of list so it becomes a list of terms.
        b = 1 # initial value of b that does not effect the value of t.
        for t in i: # This takes terms at index i in the list multplies them. 
            t,b = b,t*b
        Denominator.append(b) # This puts all terms multiplied together into list.
        
    return Denominator # Returns denominator terms from the function when Denominator function executes.
  
def Lagrange_Coefficients(GPS_DATA): # Defines the function that combines the numerator and denominator terms into one matrix.
    # Defining of Variables
    Top = Numerator(GPS_DATA) # This excutes the Numerator function
    Bottom = Denominator(GPS_DATA) # This excutes the Denominator function
    Coefficients = zeros(1,len(Top)) # This initializes a matrix filled with zeros for later storage.
    #Combination 
    for i in range(len(Top)): # Divides the ith term of Top by the ith term of bottom and assigns it to the ith location of the coefficient matrix. 
        Coefficients[i] = Top[i]/Bottom[i] 
    return Coefficients # Returns coefficient terms from the function when Lagrange Coefficients function executes.

def Lagrange_Interpolation_Polynomials(GPS_DATA): # Defines a function that generates an equation by following the Lagrange Interpolation Polynomial method. 
    Dependent_Variable = GPS_DATA[:,1] # This pulls the second colunm of the inputted GPS data.
    Equation = Lagrange_Coefficients(GPS_DATA)* Dependent_Variable # This performs a linear combination of the coefficient polynomials and the dependent variable.
    return Equation # Returns the final equation that describes the inputted GPS data. 

print(Lagrange_Interpolation_Polynomials(GPS_DATA))
#print(Lagrange_Coefficients(GPS_DATA))
#print(Denominator(GPS_DATA))
#print(Numerator(GPS_DATA))
Equation_Matrix = Lagrange_Interpolation_Polynomials(GPS_DATA)
Graph = Equation_Matrix[0]
print(Graph)
plot3d(Graph, (x,-1,1),(y,-1,1))

