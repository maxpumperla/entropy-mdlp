from math import log
import numpy as np
from bisect import bisect_right


class MDLP(object):
    '''
    Entropy-based Minimum description length principle.
    '''
    def discretize_feature(self, x, binning):
        '''
        Discretize a feature x with respective to the given binning
        '''
        x_discrete = [1 for i in range(len(x))]
        for i in range(len(x)):
            for cut_value in binning:
                if x[i] > cut_value:
                    x_discrete[i] = x_discrete[i] + 1
        return np.array(x_discrete)

    def target_table(self, target):
        '''
        Create a numpy array that counts the occurrences
        of values of the input vector
        Example:
        target_table([1,2,2,3,4,5,5,5,5,6])
        >>> array([1,2,1,1,4,1])
        '''
        return np.unique(target, return_counts=True)[1]

    def stable_log(self, input):
        '''
        Stable version of natural logarithm, which
        replaces elements smaller than 1*e^(-10) by
        one to avoid infinite values, then applies log as usual.
        The input variable has to be a numpy array.
        Example:
        stable_log([0,1,2])
        >>> array([1,2,3,4,5,6])
        '''
        copy = input.copy()
        copy[copy <= 1e-10] = 1
        return np.log(copy)
        
    def entropy(self, variable):
        '''
        Compute the Shannon entropy of the input variable
        Example:
        stable_log(np.array([0,1,2]))
        >>> array([0., 0., 0.69314718])
        '''
        prob = self.target_table(variable) / len(variable)
        ent = -sum(prob * self.stable_log(prob))
        print(ent)
        return ent

    def levels(self, variable):
        '''
        Create a numpy array that lists each value of the
        input vector once.
        Example:
        levels([1,2,2,3,4,5,5,5,5,6])
        >>> array([1,2,3,4,5,6])
        '''
        return np.unique(variable)

    def stopping_criterion(self, cut_idx, target, ent):
        '''
        Stopping criterion of the MDLP algorithm. Specifying a
        cutting index cut_idx, a target vector and the current entropy,
        the function will compute the entropy of the vector split by
        the cutting point.
        If the gain in further splitting, i.e. the decrease in entropy
        is too small, the algorithm will return "None" and MDLP will
        be stopped.
        '''
        n = len(target)
        target_entropy = self.entropy(target)
        gain = target_entropy - ent
        
        k = len(np.unique(target))
        k1 = len(np.unique(target[: cut_idx]))
        k2 = len(np.unique(target[cut_idx: ]))
        
        delta = (log(3**k - 2) - (k * target_entropy
                 - k1 * self.entropy(target[: cut_idx])
                 - k2 * self.entropy(target[cut_idx: ])))
        cond = log(n - 1) / n + delta / n
        if gain >= cond:
            return gain
        else:
            return None

    def find_cut_index(self, x, y):
        '''
        Determine the optimal cutting point (in the sense
        of minimizing entropy) for a feature vector x and
        a corresponding target vector y.
        The function will return the index of this point
        and the respective entropy.
        '''
        n = len(y)
        init_entropy = 9999
        current_entropy = init_entropy
        index = None
        for i in range(n - 1):
            if (x[i] != x[i+1]):
                cut = (x[i] + x[i + 1]) / 2.
                cutx = bisect_right(x, cut)
                weight_cutx = cutx / n
                left_entropy = weight_cutx * self.entropy(y[: cutx])
                right_entropy = (1 - weight_cutx) * self.entropy(y[cutx: ])
                temp = left_entropy + right_entropy
                if temp < current_entropy:
                    current_entropy = temp
                    index = i + 1
        if index is not None:
            return [index, current_entropy]
        else:
            return None

    def cut_points(self, x, y):
        '''
        Main function for the MDLP algorithm. A feature vector x
        and a target vector y are given as input, the algorithm
        computes a list of cut-values used for binning the variable x.
        '''
        sorted_index = np.argsort(x)
        xo = x[sorted_index]
        yo = y[sorted_index]
        depth = 1

        def getIndex(low, upp, depth=depth):
            x = xo[low:upp]
            y = yo[low:upp]
            cut = self.find_cut_index(x, y)
            if cut is None:
                return None
            cut_index = int(cut[0])
            current_entropy = cut[1]
            ret = self.stopping_criterion(cut_index, np.array(y),
                                          current_entropy)
            if ret is not None:
                return [cut_index, depth + 1]
            else:
                return None

        def part(low=0, upp=len(xo)-1, cut_points=np.array([]), depth=depth):
            x = xo[low: upp]
            if len(x) < 2:
                return cut_points
            cc = getIndex(low, upp, depth=depth)
            if (cc is None):
                return cut_points
            ci = int(cc[0])
            depth = int(cc[1])
            cut_points = np.append(cut_points, low + ci)
            cut_points = cut_points.astype(int)
            cut_points.sort()
            return (list(part(low, low + ci, cut_points, depth=depth))
                    + list(part(low + ci + 1, upp, cut_points, depth=depth)))

        res = part(depth=depth)
        cut_index = None
        cut_value = []
        if res is not None:
                cut_index = res
                for indices in cut_index:
                        cut_value.append((xo[indices-1] + xo[indices])/2.0)
        result = np.unique(cut_value)
        return result
