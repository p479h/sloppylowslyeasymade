#from masses import masses

##### parenthetic_contents #############################################
def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])

##### sort ################################################################
def sort(tup):
    tup.sort(key = lambda x: x[0])
    return tup

##### sum_1_or_2_nums #######################################################
def sum_1_or_2_nums(form, pos, mw, mass):
    ms = 0
    # check for > 9
    if form[pos:pos+2].isnumeric():
        ms += mass * int(form[pos:pos+2])
    else:
        # check for > 1
        if form[pos:pos+1].isnumeric():
            ms += mass * int(form[pos:pos+1])
        else:
            # no subscript just 1 element
            ms += mass
    return ms + mw

##### iterate_form ############################################################
def iterate_form(form):
    mw = 0
    print(f'form {form}')
    for j in range(len(form)):
        # check to see if numeric and then skip if so
        if not form[j:1].isnumeric():
            # check both 1 and 2 letter elements
            mass1 = masses.get(form[j:j+1])
            mass2 = masses.get(form[j:j+2])
            # do mass2 first and skip mass1 unless mass2 is None
            if not mass2 is None:
                mw = sum_1_or_2_nums(form, j+2, mw, mass2)
                print(f'mass2 = {form[j:j+2]}  added mw of {mw}')
            else:
                if not mass1 is None:
                    # one letter element
                    mw = sum_1_or_2_nums(form, j+1, mw, mass1)
                    print(f'mass1 = {form[j:j+1]}   added mw of {mw}')
    return mw

##### main #############################################################
#formula = 'CH(NO2)3CH(CCl3)2' # 1,1,1-trinitro-2,2-trichloroethane(unstable, probably doesn't exist, kaboom!)
formula = 'Pb(CH3CO2)4' # lead tetraacetate

l = list((parenthetic_contents(formula)))
lst = sorted(l, key = lambda x: x[1], reverse=False)

total_mw = 0
print(lst)
for i, c in enumerate(lst):
    # find the str in the formula and check the
    # next item to see if it's a number for the multiplier
    form = c[1]
    srch_str = '('+form+')'
    srch_len = len(srch_str)
    pos = formula.find(srch_str)
    if formula[pos+srch_len].isnumeric():
        multiplier = int(formula[pos+srch_len])
    else: multiplier = 1 # number outside of parenthesis
    # delete this part of the formula so last bit can be calculated
    if multiplier != 1:
        # a number is present assuming < 10
        formula = formula.replace(formula[pos:pos+srch_len+1], '')
    mw = iterate_form(form)  * multiplier
    total_mw += mw

# do the last part
mw = iterate_form(formula)
total_mw += mw

print()
print(f'total_mw {total_mw}')
#print('expected 400.79') # trinitro
print('expected 443.38') # Pb(IV) acetate

#print(list(parenthetic_contents('(a(b(c)(d)e)(f)g)')))
