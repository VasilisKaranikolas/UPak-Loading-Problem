import pyomo.environ as pyo
model = pyo.AbstractModel(name = "BA_Opt_Karanikolas_part1")

model.n = pyo.Param(within=pyo.PositiveIntegers)                    #arithmos parageliwn
model.N = pyo.RangeSet(0, model.n-1)                                #set paraggeliwn apo 0 ews n-1 
model.Price = pyo.Param(model.N)                                    #kostos kathe paragelias i
model.Size = pyo.Param(model.N)                                     #megethos kathe paragelias i

model.t = pyo.Param(within=pyo.PositiveIntegers)                    #arithmos fortigwn
model.T = pyo.RangeSet(0, model.t-1)                                #set fortigwn apo 0 ews n-1
model.Capacity = pyo.Param(model.T)                                 #xwritikothta kathe fortigou j

model.x = pyo.Var(model.N, model.T, domain=pyo.Binary)              #metavlhth apofasis 0 h 1

#antikeimeniki synarthsh
def obj_rule(model):
    return sum(model.Price[i] * model.Size[i] * model.x[i, j] for i in model.N for j in model.T)
model.obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)

#periorismos monadikothtas paragelias
def whole_orders_rule(model,i):
    return sum(model.x[i, j] for j in model.T) <= 1
model.whole_orders = pyo.Constraint(model.N, rule=whole_orders_rule)

#periorismos xwrhtikothtas
def capacity_rule(model, j):
    return sum(model.Size[i] * model.x[i, j] for i in model.N) <= model.Capacity[j]
model.capacity = pyo.Constraint(model.T, rule=capacity_rule)

#lush tou modelou me th xrhsh tou glpk solver
model = model.create_instance('BA_Opt_2023.dat')
solver = pyo.SolverFactory('glpk')
opt = solver.solve(model)

#ektypwsh twn apotelesmatwn
print("The maximum profit is: ", model.obj())
for j in model.T:
    print("")
    print("Orders assigned in truck", j, "are:")
    mass=0
    for i in model.N:
        if pyo.value(model.x[i, j]) == 1:
            mass= mass+model.Size[i]
            print("                                Order", i)
    print("The capacity used in truck", j, "is",mass,"of total",pyo.value(model.Capacity[j]), "cubic meters")

print("")
print("Orders not assigned to any truck:")

none_left = True
for i in model.N:
    assigned = False
    for j in model.T:
        if pyo.value(model.x[i, j]) == 1:
            assigned = True
            break
    if not assigned:
        print("                                Order", i)
        none_left = False
if none_left ==True:
        print("                                None") 