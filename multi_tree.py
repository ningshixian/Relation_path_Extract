#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8
'''
    树的实现上，一般都是采用链式结构
'''


class TreeNode:
    def __init__(self, value):
        self.children = []
        self.value = value
        self.parent = None

    def add_child(self, child):
        # self.children += child
        child.parent = self
        self.children.append(child)

    def get_data(self):
        return self.value

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    def go(self, data):
        for child in self.children:
            if child.getdata() == data:
                return child
        return None

    def show(self, layer):
        print  "  " * layer + self.value
        map(lambda child: child.show(layer + 1), self.children)


# def main():
#     a1 = TreeNode("A-1")
#     b1 = TreeNode("B-1")
#     c1 = TreeNode("C-1")
#     d1 = TreeNode("D-1")
#     e = TreeNode("e-1")
#     f = TreeNode("f-1")
#     g = TreeNode("g-1")
#     h = TreeNode("h-1")
#     i = TreeNode("i-1")
#     j = TreeNode("j-1")
#     k = TreeNode("k-1")
#     l = TreeNode('L')
#     m = TreeNode('M')
#     n = TreeNode('N')
#     o = TreeNode('O')
#     a1.add_child(b1, g, h)
#     b1.add_child(c1, e)
#     c1.add_child(d1, f)
#     d1.add_child(TreeNode('1'))
#     g.add_child(i, j, k, l)
#     h.add_child(m, n, o)
#     a1.show(0)
#
#
# if __name__ == "__main__": main()