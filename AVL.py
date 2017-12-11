#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 12:06:07 2017
BST tree transformed into an AVL
@author: alex
"""

import random

class Node(object):
    def __init__(self, data=None, left=None, right=None, parent=None, height=None):
        self.data = data
        self.dcounter = 1 #number of duplicates of this node
        self.height = 0 #height of current node
        self.left = left
        self.right = right
        self.parent = parent
    def getdata(self):
        return self.data
    def getleft(self):
        return self.left
    def getheight(self):
        return self.height
    def dcount(self):
        self.dcounter += 1
    def getright(self):
        return self.right
    def getparent(self):
        return self.parent
    def setparent(self, newparent):
        self.parent = newparent
    def setleft(self, newchild):
        self.left = newchild
    def setright(self, newchild):
        self.right = newchild
        
def height(node):
    if node is None:
        return -1
    else:
        return node.height
    
class Tree(object):
    def __init__(self, start=None, current=None):
        self.start = start
        self.current = current
    def height(self, current):
        current = current
        if current is None:
            return -1
        else:
            return current.height
    def update_height(self, node):
        if node is not None:
            if node.left is None and node.right is not None:
                node.height = node.right.height + 1
            elif node.left is not None and node.right is None:
                node.height = node.left.height + 1
            elif node.left is not None and node.right is not None:
                node.height = max(height(node.left), height(node.right)) + 1
                
    def RotateLeft(self,current):
        current = current
        right = current.right
        if right != None:
            right.parent = current.parent
            if right.parent is None:
                self.start = right
            else:
                if right.parent.left is current:
                    right.parent.left = right
                elif right.parent.right is current:
                    right.parent.right = right
            current.right = right.left
            if current.right is not None:
                current.right.parent = current
            right.left = current
            current.parent = right
            self.update_height(right)
        self.update_height(current)
       
    def RotateRight(self,current):
        current = current
        left = current.left
        if left != None:
            left.parent = current.parent
            if left.parent is None:
                self.start = left
            else:
                if left.parent.left is current:
                    left.parent.left = left
                elif left.parent.right is current:
                    left.parent.right = left
            current.left = left.right
            if current.left is not None:
                current.left.parent = current
            left.right = current
            current.parent = left
            self.update_height(left)
        self.update_height(current)
            
    def rebalance(self, node):
        current = node
        while current != None:
            self.update_height(current)
            if self.height(current.left) > 2 + self.height(current.right):
                if self.height(current.left.left) >= self.height(current.left.right):
                    self.RotateRight(current)
                else:
                    self.RotateLeft(current.left)
                    self.RotateRight(current)
            elif self.height(current.right) > 2 + self.height(current.left):
                if height(current.right.right) >= self.height(current.right.left):
                    self.RotateLeft(current)
                else:
                    self.RotateRight(current.right)
                    self.RotateLeft(current)
            current = current.parent
    def insert(self, dat):
        tnode = Node(dat)
        current = self.start
        if self.start == None:
            self.start = tnode
            current = self.start
        else:
            while tnode.getparent() == None:
                if tnode.getdata() < current.getdata():
                    if current.getleft() == None:
                        current.setleft(tnode)
                        tnode.setparent(current)
                    else:
                        current = current.getleft()
                elif tnode.getdata() > current.getdata():
                    if current.getright() == None:
                        current.setright(tnode)
                        tnode.setparent(current)
                    else:
                        current = current.getright()
                elif current.getdata() == tnode.getdata():
                    current.dcount()
        self.rebalance(current)
    def search(self, data):
        found = False
        current = self.start
        while found == False:
            self.current = current
            if current.getdata() == data:
                found = True
            elif data < current.getdata():
                if current.getleft() == None:
                    break
                else:
                    current = current.getleft()
            elif data > current.getdata():
                if current.getright() == None:
                    break
                else:
                    current = current.getright()
        if found == True:
            return True
        else:
            print (str(data) + " not found")
    def delete(self, data): #if the item sought is the root then will not work.
        self.search(data) #find node to delete
        current = self.current
        delparent = current.getparent() #to be deleted node's parent
        delcurrent = current #to be deleted node
        if self.search(data) == True:
            if current.getleft() == None and current.getright() == None:
                print ("leaf problem")
                if delparent.getleft() == current:
                    delparent.setleft(None)
                elif delparent.getright() == current:
                    delparent.setright(None)
            elif current.getleft()== None or current.getright()==None:
                print ("single child problem")
                if current.getleft() != None:
                    movedchild = current.getleft()
                elif current.getright() != None:
                    movedchild = current.getright()
                if delparent.getleft() == delcurrent:
                    delparent.setleft(movedchild)
                elif delparent.getright() == delcurrent:
                    delparent.setright(movedchild)
            elif current.getleft() != None and current.getright() != None:
                print ("double child problem")
                #searches for a replacement that is just less than deleted node
                current = current.getleft()
                while current.getright()!=None:
                    current = current.getright()
                if current.getleft() != None: #makes replacement a leaf
                    self.RotateRight(current)
                #deletes the replacement's parent's path to the replacement
                if current.getparent().getleft() == current:
                    current.getparent().setleft(None)
                elif current.getparent().getright() == current:
                    current.getparent().setright(None)
                #checks the paths of the deleted node's parent to confirm which
                #side it is and place the replacement
                if delparent.getleft() == delcurrent:
                    delparent.setleft(current)
                    current.setparent(delparent)
                    current.setright(delcurrent.right)
                    current.setleft(delcurrent.left)
                elif delparent.getright() == delcurrent:
                    delparent.setright(current)
                    current.setparent(delparent)
                    current.setright(delcurrent.right)
                    current.setleft(delcurrent.left)
            print ("Data: ("+str(data)+") found and removed")
        else:
            print ("data not found or deleted")
        self.rebalance(delparent)
        self.rebalance(delparent.right)
        self.rebalance(delparent.left)
    def __str__(self):
        if self.start is None: return '<empty tree>'
        def recurse(node):
            if node is None: return [], 0, 0
            label = str(node.data)
            left_lines, left_pos, left_width = recurse(node.left)
            right_lines, right_pos, right_width = recurse(node.right)
            middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
            pos = left_pos + middle // 2
            width = left_pos + middle + right_width - right_pos
            while len(left_lines) < len(right_lines):
                left_lines.append(' ' * left_width)
            while len(right_lines) < len(left_lines):
                right_lines.append(' ' * right_width)
            if (middle - len(label)) % 2 == 1 and node.parent is not None and \
               node is node.parent.left and len(label) < middle:
                label += '.'
            label = label.center(middle, '.')
            if label[0] == '.': label = ' ' + label[1:]
            if label[-1] == '.': label = label[:-1] + ' '
            lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                     ' ' * left_pos + '/' + ' ' * (middle-2) +
                     '\\' + ' ' * (right_width - right_pos)] + \
              [left_line + ' ' * (width - left_width - right_width) +
               right_line
               for left_line, right_line in zip(left_lines, right_lines)]
            return lines, pos, width
        return '\n'.join(recurse(self.start) [0])                       
   
tre = Tree()
testdata = list(random.sample(range(30,201), 70))
for dat in testdata:
    tre.insert(dat)

print (tre.__str__())
print ("")
#test functions
inp = int(input ("Enter number to delete: "))
tre.delete(inp) 
tre.search(inp)
print (tre.__str__())
inp = input ("press 'enter' to close")
