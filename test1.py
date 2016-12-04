a=[1,5,2,3,8]
b=[1,2,3,4,5,6,7,8,9]
# for x in a:
#   if x not in b:
#       return False
#   return True

def check(a,b):
    for x in a:
        if x not in b:
            return False
        return True


print(check([1, 5, 2, 3, 8],[1, 2, 3, 4, 5, 6, 7, 8, 9]))