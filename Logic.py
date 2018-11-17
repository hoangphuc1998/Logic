import sys
class Term:
    #Constant or variable
    def __init__(self, term):
        self.is_var = self.is_variable(term)
        self.term = term
    def __str__(self):
        return str(self.term)
    def is_variable(self,term):
        if term.islower():
            return False
        else:
            return True
    def __eq__(self, cmp):
        return self.is_var == cmp.is_var and self.term == cmp.term
    

class Statement:
    def __init__(self, list_of_terms = [], predicate = '', negative = False):
        self.list_of_terms = list_of_terms
        self.predicate = predicate
        self.negative = negative
    def negate(self):
        return Statement(list_of_terms=self.list_of_terms, predicate=self.predicate, negative = not self.negative)
    def add_new_term(self,term):
        self.list_of_terms.append(term)
    def simplify(self):
        if len(self.list_of_terms)==1 and isinstance(self.list_of_terms[0],Conjunction):
            self.list_of_terms = self.list_of_terms[0].list_of_statements
    def __str__(self):
        output = self.predicate + '('
        for term in self.list_of_terms:
            output += str(term) + ', '
        output = output[:-2]+')'
        return output
    def __eq__(self, cmp):
        equal = True
        if len(self.list_of_terms)!=len(cmp.list_of_terms):
            return False
        else:
            for i in range(len(self.list_of_terms)):
                if not self.list_of_terms[i] == cmp.list_of_terms[i]:
                    equal = False
                    break
        return self.predicate == cmp.predicate and self.negative == cmp.negative and equal
    def is_identical(self,cmp):
        equal = True
        if len(self.list_of_terms)!=len(cmp.list_of_terms):
            return False
        else:
            for i in range(len(self.list_of_terms)):
                if self.list_of_terms[i].is_var == False and cmp.list_of_terms[i].is_var == False \
                and not self.list_of_terms[i] == cmp.list_of_terms[i]:
                    equal = False
                    break
        return self.predicate == cmp.predicate and self.negative == cmp.negative and equal
    def is_unificable(self,obj):
        return self.predicate == obj.predicate and self.negative == obj.negative and \
        len(self.list_of_terms) == len(obj.list_of_terms)

class Conjunction:
    #Conjunction of statements
    def __init__(self, list_of_statements = []):
        self.list_of_statements = list_of_statements
    def negate(self):
        new_statements = []
        for statement in self.list_of_statements:
            new_statements.append(statement.negate())
        return Disjunction(new_statements)
    def add_new_statement(self, statement):
        self.list_of_statements.append(statement)
    def simplify(self):
        index = 0
        while index < len(self.list_of_statements):
            if isinstance(self.list_of_statements[index],Conjunction):
                self.list_of_statements[index].simplify()
                l = len(self.list_of_statements[index].list_of_statements)
                for i,statement in enumerate(self.list_of_statements[index].list_of_statements):
                    self.list_of_statements.insert(index + i + 1,statement)
                del self.list_of_statements[index]
                index+=l-1
            elif isinstance(self.list_of_statements[index],Disjunction):
                self.list_of_statements[index].simplify()
            index+=1

    def __str__(self):
        output = '('
        for statement in self.list_of_statements:
            output+=str(statement)+' & '
        return output[:-3]+')'
    def __eq__(self,cmp):
        if len(self.list_of_statements) != len(cmp.list_of_statements):
            return False
        else:
            equal = True
            for i in range(len(self.list_of_statements)):
                if not self.list_of_statements[i] == cmp.list_of_statements[i]:
                    equal = False
                    break
            return equal
class Disjunction:
    #Disjunction of statements
    def __init__(self, list_of_statements = []):
        self.list_of_statements = list_of_statements
    def negate(self):
        new_statements = []
        for statement in self.list_of_statements:
            new_statements.append(statement.negate())
        return Conjunction(new_statements)
    def add_new_statement(self, statement):
        self.list_of_statements.append(statement)
    def __str__(self):
        output = '('
        for statement in self.list_of_statements:
            output+=str(statement)+' | '
        return output[:-3]+')'
    def simplify(self):
        index = 0
        while index < len(self.list_of_statements):
            if isinstance(self.list_of_statements[index],Disjunction):
                self.list_of_statements[index].simplify()
                l = len(self.list_of_statements[index].list_of_statements)
                for i,statement in enumerate(self.list_of_statements[index].list_of_statements):
                    self.list_of_statements.insert(index + i + 1,statement)
                del self.list_of_statements[index]
                index+=l-1
            elif isinstance(self.list_of_statements[index],Conjunction):
                self.list_of_statements[index].simplify()
            index+=1
    def __eq__(self,cmp):
        if len(self.list_of_statements) != len(cmp.list_of_statements):
            return False
        else:
            equal = True
            for i in len(self.list_of_statements):
                if not self.list_of_statements[i] == cmp.list_of_statements[i]:
                    equal = False
                    break
            return equal
class Rule:
    #Define a rule with left and right hand side are Conjunction of statements
    def __init__(self, lhs, rhs = None):
        self.lhs = lhs
        self.rhs = rhs
        self.is_used = False
    def __str__(self):
        return str(self.lhs) + ' -> ' + str(self.rhs)

def is_operator(c):
    return c=='&' or c == '|'
def is_higher_precedence(a,b):
    return a == '&' and b == '|'

#Change to Reverse Polish Notation
def change_to_RPN(tokens):
    operator_stack = []
    output = []
    for token in tokens:
        if token == '(':
            operator_stack.append(token)
        elif token == ')':
            operator = operator_stack.pop()
            while operator != '(':
                output.append(operator)
                operator = operator_stack.pop()
        elif is_operator(token):
            while len(operator_stack)>0 and (operator_stack[-1].endswith('*') or \
            is_higher_precedence(operator_stack[-1],token) or operator_stack[-1]==token) and (operator_stack[-1]!='('):
                output.append(operator_stack.pop())
            operator_stack.append(token)
        else:
            if token.endswith('*'):
                operator_stack.append(token)
            else:
                output.append(token)
    operator_stack.reverse()
    output = output + operator_stack
    return output

#Process RPN and convert to conjunction
def convert_to_conjunction(tokens):
    stack = []
    for token in tokens:
        if token.endswith('*'):
            operands = stack.pop()
            operands = operands.term.split(',')
            list_of_terms = []
            for operand in operands:
                list_of_terms.append(Term(operand))
            statement = Statement(list_of_terms=list_of_terms,predicate=token[:-1])
            stack.append(statement)
        elif is_operator(token):
            list_of_statements = []
            list_of_statements.append(stack.pop())
            list_of_statements.append(stack.pop())
            list_of_statements.reverse()
            new_operand = []
            if token == '&':
                new_operand = Conjunction(list_of_statements=list_of_statements)
            elif token == '|':
                new_operand = Disjunction(list_of_statements=list_of_statements)
            stack.append(new_operand)
        else:
            stack.append(Term(token))
    output = Conjunction([stack.pop()])
    output.simplify()
    return output

def process_string(s):
    #Turn string to list of tokens
    tokens = []
    name = ''
    for ch in s:
        if is_operator(ch) or ch == '(' or ch == ')':
            if name!='':
                if ch == '(':
                    name += '*'
                tokens.append(name)
                name = ''
            tokens.append(ch)
        elif ch==' ':
            continue
        else:
            name+=ch
    rpn = change_to_RPN(tokens)
    print(rpn)
    output_line = convert_to_conjunction(rpn)
    return output_line

class Binding:
    def __init__(self):
        self.binding_dict = {}
        self.is_fail = False
    def add_new_binding(self, key, value):
        #Key and value is term
        self.binding_dict[key.term] = value.term
    def already_has(self, key):
        return key.term in self.binding_dict
    def bind(self,x):
        if isinstance(x,Term):
            if x.term in self.binding_dict:
                return Term(self.binding_dict[x.term])
            else:
                return x
        elif isinstance(x,Statement):
            list_of_terms = []
            for term in x.list_of_terms:
                list_of_terms.append(self.bind(term))
            return Statement(list_of_terms=list_of_terms,predicate=x.predicate)
        elif isinstance(x,Conjunction):
            list_of_statements = []
            for statement in x.list_of_statements:
                list_of_statements.append(self.bind(statement))
            return Conjunction(list_of_statements=list_of_statements)
        elif isinstance(x,Disjunction):
            list_of_statements = []
            for statement in x.list_of_statements:
                list_of_statements.append(self.bind(statement))
            return Disjunction(list_of_statements=list_of_statements)
    
class KnowledgeBase:
    #Knowledge Base with set of rules (facts are rules without right hand side)
    def __init__(self):
        self.list_of_rules = []
        self.list_of_facts = []
    def input_from_file(self, filename):
        with open(filename,'r') as f:
            line = f.readline()
            while line!='':
                expr = line.split(':-')
                print(expr[0])
                new_rule = None
                if len(expr) == 2:
                    new_rule = Rule(process_string(expr[0]), process_string(expr[1]))
                    self.list_of_rules.append(new_rule)
                elif len(expr)==1:
                    new_rule = Rule(process_string(expr[0]))
                    self.list_of_facts.append(new_rule)
                line = f.readline()
            
    def __str__(self):
        output = ''
        for rule in self.list_of_rules:
            output+= str(rule) + '\n'
        for fact in self.list_of_facts:
            output+= str(fact) + '\n'
        return output

def unify(x,y, binding):
    if binding.is_fail:
        return binding
    elif x == y:
        return binding
    elif isinstance(x,Term) and x.is_var:
        return unify_var(x,y,binding)
    elif isinstance(y,Term) and y.is_var:
        return unify_var(y,x,binding)
    elif isinstance(x,Statement) and isinstance(y,Statement):
        if x.is_unificable(y):
            return unify(x.list_of_terms,y.list_of_terms,binding)
    elif (isinstance(x,Conjunction) and isinstance(y,Conjunction)) or (isinstance(x,Disjunction) and isinstance(y,Disjunction)):
        if len(x.list_of_statements)==len(y.list_of_statements):
            return unify(x.list_of_statements,y.list_of_statements,binding)
    elif isinstance(x,list) and isinstance(y,list):
        if len(x) == len(y):
            return unify(x[0],y[0],unify(x[1:],y[1:],binding))
    else:
        binding.is_fail = True
        return binding

def unify_var(var,x,binding):
    if binding.already_has(var):
        return unify(binding.bind(var),x,binding)
    elif binding.already_has(x):
        return unify(var,binding.bind(x),binding)
    else:
        binding.add_new_binding(var,x)
        return binding

def forward_chaining(knowledge_base,question):
    while True:
        new = []

knowledge_base = KnowledgeBase()
knowledge_base.input_from_file('input.txt')
print(str(knowledge_base))
binding = Binding()
unify(knowledge_base.list_of_facts[0].lhs,knowledge_base.list_of_facts[1].lhs,binding)
print(binding.is_fail)
print(binding.binding_dict)
print(str(binding.bind(knowledge_base.list_of_facts[0].lhs)))
print(str(binding.bind(knowledge_base.list_of_facts[1].lhs)))
print(binding.bind(knowledge_base.list_of_facts[0].lhs)==binding.bind(knowledge_base.list_of_facts[1].lhs))