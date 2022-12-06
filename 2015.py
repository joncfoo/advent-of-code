#!/usr/bin/env python3

import collections
import hashlib

def day1():
	with open('data/2015-01') as f:
		data = f.read()
	floor = 0
	position = None
	directions = {'(': 1, ')': -1}

	for index, direction in enumerate(data):
		if position is None and floor == -1:
			position = index
		floor += directions[direction]

	print(f'2015-01: {floor} {position}')


def day2():
	with open('data/2015-02') as f:
		data = [line.strip() for line in f.readlines()]
	data = [line.split('x') for line in data]
	data = [sorted([int(l), int(w), int(h)]) for (l,w,h) in data]
	sqft_paper = 0
	ribbon = 0

	for (l,w,h) in data:
		sqft_paper += 2*l*w + 2*w*h + 2*h*l + l*w
		ribbon += 2*l+2*w + l*w*h

	print(f'2015-02: {sqft_paper} {ribbon}')


def day3():
	with open('data/2015-03') as f:
		data = f.read()

	def visit(directions):
		houses = set()
		houses.add((0,0))
		(x,y) = (0,0)
		for direction in directions:
			match direction:
				case '>':
					x+=1
				case '<':
					x-=1
				case '^':
					y-=1
				case 'v':
					y+=1
			houses.add((x,y))
		return houses

	part1 = len(visit(data))
	santa_directions = [d for (i, d) in enumerate(data) if i % 2 == 0]
	robot_directions = [d for (i, d) in enumerate(data) if i % 2 == 1]
	part2 = len(visit(santa_directions) | visit(robot_directions))

	print(f'2015-03: {part1} {part2}')


def day4():
	data = 'bgvyzdsv'
	x = 0
	(five, six) = (0, 0)

	while five == 0 or six == 0:
		digest = hashlib.md5(f'{data}{x}'.encode()).hexdigest()
		if six == 0 and digest.startswith('000000'):
			six = x
		elif five == 0 and digest.startswith('00000'):
			five = x
		x+=1

	print(f'2015-04: {five} {six}')


def day5():
	with open('data/2015-05') as f:
		data = [line.strip() for line in f.readlines()]

	def part1_is_nice(line):
		vowels = 0
		twice = 0
		for i in range(len(line)-1):
			if line[i] in 'aeiou':
				vowels+=1
			if line[i] == line[i+1]:
				twice+= 1
			if line[i]+line[i+1] in {'ab', 'cd', 'pq', 'xy'}:
				return False
		if line[i+1] in 'aeiou':
			vowels+=1
		return vowels > 2 and twice > 0

	def part2_is_nice(line):
		def pairs(line):
			counts = collections.defaultdict(int)
			overlap = False
			previous = ''
			for i in range(1, len(line)):
				pair = line[i-1]+line[i]
				if pair == previous:
					if not overlap:
						overlap = True
						continue
				counts[pair] += 1
				previous = pair
			return max(counts.values()) > 1

		def surround(line):
			for i in range(2, len(line)):
				if line[i-2] == line[i]:
					return True
			return False
		return pairs(line) and surround(line)

	part1 = len(list(filter(part1_is_nice, data)))
	part2 = len(list(filter(part2_is_nice, data)))
	print(f'2015-05: {part1} {part2}')


def day6():
	with open('data/2015-06') as f:
		data = [line.strip() for line in f.readlines()]
	g1 = [[0 for a in range(1000)] for b in range(1000)]
	g2 = [[0 for a in range(1000)] for b in range(1000)]
	def update(grid, fn, x1, y1, x2, y2):
		for x in range(x1, x2+1):
			for y in range(y1, y2+1):
				grid[x][y] = fn(grid[x][y])
	for line in data:
		parts = line.split(' ')
		if parts[0] == 'turn':
			(x1,y1) = map(int,parts[2].split(','))
			(x2,y2) = map(int,parts[4].split(','))
			if parts[1] == 'on':
				fn1 = lambda _: 1
				fn2 = lambda n: n+1
			else:
				fn1 = lambda _: 0
				fn2 = lambda n: max(n-1, 0)
		else:
			(x1,y1) = map(int,parts[1].split(','))
			(x2,y2) = map(int,parts[3].split(','))
			fn1 = lambda n: n^1
			fn2 = lambda n: n+2
		update(g1, fn1, x1, y1, x2, y2)
		update(g2, fn2, x1, y1, x2, y2)
	part1=0
	part2=0
	for x in range(0, 1000):
		for y in range(0, 1000):
			if g1[x][y] == 1:
				part1+=1
			part2 += g2[x][y]
	print(f'2015-06: {part1} {part2}')


def day7():
	with open('data/2015-07') as f:
		data = [line.strip() for line in f.readlines()]
	signals = {}
	for line in data:
		parts = line.split(' ')
		(var, expression) = (parts[-1], parts[0:len(parts)-2])
		signals[var] = list(map(lambda x: int(x) if x[0].isdigit() else x, expression))
	for k,v in signals.items():
		if len(v) == 1:
			signals[k] = v[0]

	def eval(expr):
		match expr:
			case [left, 'AND', right]:
				return eval(left) & eval(right)
			case [left, 'OR', right]:
				return eval(left) | eval(right)
			case [left, 'LSHIFT', right]:
				return eval(left) << right
			case [left, 'RSHIFT', right]:
				return eval(left) >> right
			case [x]:
				return eval(signals[x])
			case ['NOT', var]:
				return eval([var]) ^ 0xFFFF
			case other:
				if type(other) is str:
					res = signals[other]
					if type(res) is int:
						return res
					else:
						res = eval(res)
						signals[other] = res
						return res
				elif type(other) is int:
					return other
				print(f'not implemented: "{other}"')
				raise Exception('not implemented')

	part1 = eval('a')
	print(f'2015-07: {part1}')
	# for part2, replace "b" value in data with part1 answer and re-run


#for d in range(1,26):
#	method = globals().get(f'day{d}')
#	if method:
#		method()

day7()
