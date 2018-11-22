import sys
import time
name_identity = 1000
class Term:
    #Constant or variable
    def __init__(self, term):
        term = term.strip()
        self.is_var = self.is_variable(term)
        self.term = term
    def __str__(self):
        return str(self.term)
    def is_variable(self,term):
        if term[0].isupper() or term.startswith('_'):
            return True
        else:
            return False
    def __eq__(self, cmp):
        return self.is_var == cmp.is_var and self.term == cmp.term
    

class Statement:
    def __init__(self, list_of_terms = [], predicate = '', negative = False):
        self.list_of_terms = []
        for term in list_of_terms:
            self.list_of_terms.append(Term(term.term))
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
    def standardlize_variable(self,bind_dict = {}):
        global name_identity
        for index, term in enumerate(self.list_of_terms):
            if term.is_var:
                if not term.term in bind_dict:
                    name_identity += 1
                    bind_dict[term.term] = '_' + str(name_identity)
                self.list_of_terms[index] = Term(term = bind_dict[term.term])
        return bind_dict

class Conjunction:
    #Conjunction of statements
    def __init__(self, list_of_statements = []):
        self.list_of_statements = []
        for statement in list_of_statements:
            if isinstance(statement,Statement):
                self.list_of_statements.append(Statement(predicate = statement.predicate,\
                list_of_terms = statement.list_of_terms, negative = statement.negative))
            elif isinstance(statement,Conjunction):
                self.list_of_statements.append(Conjunction(statement.list_of_statements))
            elif isinstance(statement,Disjunction):
                self.list_of_statements.append(Disjunction(statement.list_of_statements))
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
    def split(self):
        list_of_new_con = []
        has_dis = False
        for index,statement in enumerate(self.list_of_statements):
            if isinstance(statement,Disjunction):
                has_dis = True
                for statement_dis in statement.list_of_statements:
                    new_list = self.list_of_statements.copy()
                    new_list[index] = statement_dis
                    new_conj = Conjunction(new_list)
                    new_conj.simplify()
                    list_of_new_con = list_of_new_con + new_conj.split()
                break
        if has_dis == False:
            list_of_new_con.append(self)
        return list_of_new_con

          
class Disjunction:
    #Disjunction of statements
    def __init__(self, list_of_statements = []):
        self.list_of_statements = []
        for statement in list_of_statements:
            if isinstance(statement,Statement):
                self.list_of_statements.append(Statement(predicate = statement.predicate,\
                list_of_terms = statement.list_of_terms, negative = statement.negative))
            elif isinstance(statement,Conjunction):
                self.list_of_statements.append(Conjunction(statement.list_of_statements))
            elif isinstance(statement,Disjunction):
                self.list_of_statements.append(Disjunction(statement.list_of_statements))
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
            output+=str(statement)+' ; '
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
            for i in range(len(self.list_of_statements)):
                if not self.list_of_statements[i] == cmp.list_of_statements[i]:
                    equal = False
                    break
            return equal
class Rule:
    #Define a rule with left and right hand side are Conjunction of statements
    def __init__(self, lhs, rhs = None):
        self.lhs = lhs
        self.rhs = rhs
        self.difference = []
        self.supported = [[] for _ in range(len(rhs.list_of_statements))]
    def __str__(self):
        return str(self.lhs) + ' <- ' + str(self.rhs)
    def split(self):
        list_of_new_rules = []
        new_conj = self.rhs.split()
        for conj in new_conj:
            list_of_new_rules.append(Rule(Statement(list_of_terms=self.lhs.list_of_terms,predicate = self.lhs.predicate, negative = self.lhs.negative),conj))
        return list_of_new_rules
    def get_supported_fact(self,list_of_facts):
        for index in range(len(self.rhs.list_of_statements)):
            for fact in list_of_facts:
                if fact.is_unificable(self.rhs.list_of_statements[index]):
                    self.supported[index].append(fact)
    def standardlize_variable(self):
        bind_dict = {}
        bind_dict = self.lhs.standardlize_variable(bind_dict=bind_dict)
        for statement in self.rhs.list_of_statements:
            bind_dict = statement.standardlize_variable(bind_dict=bind_dict)
        for difference in self.difference:
            difference[0].term = bind_dict[difference[0].term]
            difference[1].term = bind_dict[difference[1].term]
    def list_supported_facts(self):
        support_list = [[]]
        for fact_list in self.supported:
            if len(fact_list) == 0:
                return []
            else:
                new = []
                for fact in fact_list:
                    for sublist in support_list:
                        new_sublist = []
                        for statement in sublist:
                            new_sublist.append(Statement(predicate= statement.predicate, negative = statement.negative,\
                            list_of_terms = statement.list_of_terms))
                        new_sublist.append(fact)
                        new.append(new_sublist)
                support_list = new
        return support_list
    def check_difference(self, binding):
        differ = True
        for difference in self.difference:
            if binding.bind(difference[0]) == binding.bind(difference[1]):
                differ = False
                break
        return differ
    def eliminate_difference(self):
        for index,statement in enumerate(self.rhs.list_of_statements):
            if statement.predicate =='\=':
                self.difference.append([Term(statement.list_of_terms[0].term),Term(statement.list_of_terms[1].term)])
                del self.rhs.list_of_statements[index]
                del self.supported[index]


def is_operator(c):
    return c=='&' or c == ';'
def is_higher_precedence(a,b):
    return a == '&' and b == ';'

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
            elif token == ';':
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
    #print(rpn)
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
            return Statement(list_of_terms=list_of_terms,predicate=x.predicate, negative = x.negative)
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
    def merge(self,obj):
        res = Binding()
        if self.is_fail or obj.is_fail:
            res.is_fail = True
        else:
            is_fail = False
            for key in self.binding_dict.keys():
                if key in obj.binding_dict and obj.binding_dict[key] != self.binding_dict[key]:
                    is_fail = True
                    break
            if is_fail:
                res.is_fail = True
            else:
                res.binding_dict.update(self.binding_dict)
                res.binding_dict.update(obj.binding_dict)
        return res
    
class ListOfBinding:
    def __init__(self, binding_list = []):
        if isinstance(binding_list,Binding):
            binding_list = [binding_list]
        self.binding_list = binding_list
    def merge_or(self, obj):
        if isinstance(obj,Binding):
            obj = ListOfBinding(binding_list=[obj])
        new_binding_list = []
        for binding in self.binding_list:
            if not binding.is_fail:
                new_binding_list.append(binding)
        for binding in obj.binding_list:
            if not binding.is_fail:
                new_binding_list.append(binding)
        return ListOfBinding(new_binding_list)
    def merge_and(self,obj):
        if isinstance(obj,Binding):
            obj = ListOfBinding(binding_list=[obj])
        new_binding_list = []
        for self_bind in self.binding_list:
            for obj_bind in obj.binding_list:
                if not self_bind.is_fail and not obj_bind.is_fail:
                    new_binding_list.append(self_bind.merge(obj_bind))
        return ListOfBinding(new_binding_list)
            

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
class KnowledgeBase:
    #Knowledge Base with set of rules (facts are rules without right hand side)
    def __init__(self):
        self.list_of_rules = []
        self.list_of_facts = []
        self.list_of_query = []
    def input_from_file(self, filename):
        with open(filename,'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('?-'):
                    line = line[2:].strip()
                    self.list_of_query.append(process_string(line).list_of_statements[0])
                elif not line.startswith('%') and line != '':
                    expr = line.split(':-')
                    #print(expr[0])
                    new_rule = None
                    if len(expr) == 2:
                        new_rule = Rule(process_string(expr[0]).list_of_statements[0], process_string(expr[1]))
                        self.list_of_rules.append(new_rule)
                    elif len(expr)==1:
                        new_rule = process_string(expr[0]).list_of_statements[0]
                        new_rule.standardlize_variable()
                        self.list_of_facts.append(new_rule)
        # Split rule
        list_of_new_rule = []
        for rule in self.list_of_rules:
            list_of_new_rule = list_of_new_rule + rule.split()
        self.list_of_rules = list_of_new_rule
        # Get supported fact for each rule
        for rule in self.list_of_rules:
            rule.eliminate_difference()
            rule.get_supported_fact(self.list_of_facts)
            rule.standardlize_variable()
    
    def __str__(self):
        output = ''
        for rule in self.list_of_rules:
            output+= str(rule) + '\n'
        for fact in self.list_of_facts:
            output+= str(fact) + '\n'
        return output
    def forward_chaining(self,goal):
        for fact in self.list_of_facts:
            if fact.is_unificable(goal):
                binding = Binding()
                unify(fact,goal,binding)
                if not binding.is_fail:
                    return binding
        while True:
            new = []
            for rule in self.list_of_rules:
                supported_facts_list = rule.list_supported_facts()
                if len(supported_facts_list)==0:
                    continue
                for fact_list in supported_facts_list:
                    new_conj = Conjunction(fact_list)
                    binding = Binding()
                    unify(rule.rhs,new_conj,binding)
                    if not binding.is_fail and rule.check_difference(binding):
                        new_fact = binding.bind(rule.lhs)
                        already_has = False
                        for fact in new:
                            if fact.is_identical(new_fact):
                                already_has = True
                                break
                        if not already_has:
                            for fact in knowledge_base.list_of_facts:
                                if fact.is_identical(new_fact):
                                    already_has = True
                                    break
                        if not already_has:
                            new.append(new_fact)
                            if goal.is_unificable(new_fact):
                                goal_bind = Binding()
                                unify(goal,new_fact,goal_bind)
                                if not goal_bind.is_fail:
                                    return goal_bind
            self.list_of_facts += new
            for rule in self.list_of_rules:
                rule.get_supported_fact(new)
            if len(new)==0:
                break
        return False
    # Backward chaining
    def backward_chaining_ask(self,goal):
        return self.backward_chaining_or(goal)
    def backward_chaining_or(self,goal):
        binding_list = ListOfBinding()
        for fact in self.list_of_facts:
            if fact.is_unificable(goal):
                binding = Binding()
                unify(fact,goal,binding)
                if not binding.is_fail:
                    binding_list.binding_list.append(binding)
        for rule in self.list_of_rules:
            if rule.lhs.is_unificable(goal):
                binding = Binding()
                unify(rule.lhs, goal, binding)
                if not binding.is_fail:
                    binding_list = binding_list.merge_or(self.backward_chaining_and(rule.rhs))
        return binding_list
    def backward_chaining_and(self, conj_of_goals):
        binding_list = ListOfBinding()
        


knowledge_base = KnowledgeBase()
knowledge_base.input_from_file('input.txt')
print(str(knowledge_base))
start = time.time()
for query in knowledge_base.list_of_query:
    binding = knowledge_base.forward_chaining(query)
    if binding == False:
        print('false.')
    else:
        for term in query.list_of_terms:
            if term.is_var:
                print(term.term + ' = ' + binding.binding_dict[term.term])
        print('true.')
end = time.time()
print(str(end - start))
# binding = Binding()
# unify(knowledge_base.list_of_rules[0].rhs,knowledge_base.list_of_rules[1].rhs,binding)
# print(binding.is_fail)
# print(binding.binding_dict)