%Define parent relationship level 0
parent(queen_elizabeth, prince_charles).
parent(queen_elizabeth, princess_anne).
parent(queen_elizabeth, prince_andrew).
parent(queen_elizabeth, prince_edward).

parent(prince_phillip, prince_charles).
parent(prince_phillip, princess_anne).
parent(prince_phillip, prince_andrew).
parent(prince_phillip, prince_edward).

%Define parent relationship level 1, from left to right
%1
parent(princess_diana, prince_william).
parent(princess_diana, prince_harry).

parent(prince_charles, prince_william).
parent(prince_charles, prince_harry).

%2
parent(captain_mark_phillips, peter_phillips).
parent(captain_mark_phillips, zara_phillips).

parent(princess_anne, peter_phillips).
parent(princess_anne, zara_phillips).

%3
parent(sarah_ferguson, princess_beatrice).
parent(sarah_ferguson, princess_eugenie).

parent(prince_andrew, princess_beatrice).
parent(prince_andrew, princess_eugenie).

%4
parent(sophie_rhys_jones, james).
parent(sophie_rhys_jones, lady_louise).

parent(prince_edward, james).
parent(prince_edward, lady_louise).

%Define parent relationship level 2, from left to right
%1
parent(prince_william, prince_george).
parent(prince_william, princess_charlotte).

parent(kate_middleton, prince_george).
parent(kate_middleton, princess_charlotte).

%2
parent(autumn_kelly, savannah_phillips).
parent(autumn_kelly, isla_phillips).

parent(peter_phillips, savannah_phillips).
parent(peter_phillips, isla_phillips).

%3
parent(zara_phillips, mia_grace_tindall).

parent(mike_tindall, mia_grace_tindall).

%Define gender

%male
male(prince_phillip).
male(prince_charles).
male(captain_mark_phillips).
male(timothy_laurence).
male(prince_andrew).
male(prince_edward).
male(prince_william).
male(prince_harry).
male(peter_phillips).
male(mike_tindall).
male(james).
male(prince_george).

%female
female(queen_elizabeth).
female(princess_diana).
female(camilla_parker_bowles).
female(princess_anne).
female(sarah_ferguson).
female(sophie_rhys_jones).
female(kate_middleton).
female(autumn_kelly).
female(zara_phillips).
female(princess_beatrice).
female(princess_eugenie).
female(lady_louise).
female(princess_charlotte).
female(savannah_phillips).
female(isla_phillips).

%married
married(queen_elizabeth, prince_phillip).
married(prince_charles, camilla_parker_bowles).
married(princess_anne, timothy_laurence).
married(sophie_rhys_jones, prince_edward).
married(prince_william, kate_middleton).
married(autumn_kelly, peter_phillips).
married(zara_phillips, mike_tindall).

married(prince_phillip, queen_elizabeth).
married(camilla_parker_bowles, prince_charles).
married(timothy_laurence, princess_anne).
married(prince_edward, sophie_rhys_jones).
married(kate_middleton, prince_william).
married(peter_phillips, autumn_kelly).
married(mike_tindall, zara_phillips).

%married(Y, X) :- married(X, Y).

%divorced
divorced(princess_diana, prince_charles).
divorced(captain_mark_phillips, princess_anne).
divorced(sarah_ferguson,prince_andrew).

divorced(prince_charles, princess_diana).
divorced(princess_anne, captain_mark_phillips).
divorced(prince_andrew, sarah_ferguson).

%divorced(Y, X) :- divorced(X, Y).

husband(Husband, Wife) :- married(Husband, Wife), male(Husband).
wife(Wife, Husband) :- married(Husband, Wife), female(Wife).
father(Parent, Child) :- parent(Parent, Child), male(Parent).
mother(Parent, Child) :- parent(Parent, Child), female(Parent).
child(Child, Parent) :- parent(Parent, Child).
son(Child, Parent) :- parent(Parent, Child), male(Child).
daughter(Child, Parent) :- parent(Parent, Child), female(Child).

grandparent(GP, GC) :- parent(GP, Parent), parent(Parent, GC).
grandmother(GM, GC) :- parent(GM, Parent), parent(Parent, GC), female(GM).
grandfather(GF, GC) :- parent(GF, Parent), parent(Parent, GC), male(GF).
grandchild(GC, GP) :- parent(GP, Parent), parent(Parent, GC).
grandson(GS, GP) :- parent(GP, Parent), parent(Parent, GS), male(GS).
granddaughter(GD, GP) :- parent(GP, Parent), parent(Parent, GD), female(GD).

sibling(Person1, Person2) :- father(Father,Person1), mother(Mother,Person1),father(Father,Person2),mother(Mother,Person2),Person1\=Person2.
brother(Person, Sibling) :- sibling(Person, Sibling),male(Person).
sister(Person, Sibling) :- sibling(Person,Sibling),female(Person).
aunt(Person, NieceNephew) :- parent(Parent,NieceNephew),(sister(Person,Parent);(brother(Uncle,Parent),wife(Person,Uncle))).
uncle(Person, NieceNephew) :- parent(Parent,NieceNephew), (brother(Person,Parent);(sister(Aunt,Parent),husband(Person,Aunt))).
niece(Person, AuntUncle) :- (aunt(AuntUncle,Person);uncle(AuntUncle,Person)),female(Person).
nephew(Person, AuntUncle) :- (aunt(AuntUncle,Person);uncle(AuntUncle,Person)),male(Person).











