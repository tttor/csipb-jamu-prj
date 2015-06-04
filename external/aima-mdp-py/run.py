from mdp import *

def main():
	m = Fig[17,1]
	
	# Solving an MDP by value iteration
	print 'Solving an MDP by value iteration'
	pi = best_policy(m, value_iteration(m, .01))
	# print pi
	# print m.to_arrows(pi)
	print_table(m.to_arrows(pi))

	# Solving an MDP by policy iteration
	print 'Solving an MDP by policy iteration'
	pi_pi = policy_iteration(m)
	print_table(m.to_arrows(pi_pi))

if __name__ == '__main__':
	main()