"""
dbscan.py

Author: Chase Davis
E-mail: cdavis@cironline.org
Web: http://labs.cironline.org

This is a simple implementation of the DBSCAN clustering algorithm implemented
as closely as possible to the pseudocode laid out in the DBSCAN Wikipedia page:

http://en.wikipedia.org/wiki/DBSCAN

DBSCAN is a popular algorithm for finding clusters in sets of data. Unlike algorithms
such as K-Means, DBSCAN does not require the user to define the number of clusters
in advance. Instead, it locates them based on point density and two inputs: a
search radius and minimum cluster size.

This implementation was designed to be as bare-bones as possible. It borrows from
a couple more robust implementations, which you'll find here:

https://github.com/mrkschan/py-dbscan/
http://code.google.com/p/education-data-ma/source/browse/trunk/data+analysis/clustering/dbscan.js?r=217

Results were checked against test data generated here:

http://people.cs.nctu.edu.tw/~rsliang/dbscan/testdatagen.html
"""
import math

class DBSCAN(object):
    """
    Simple implementation of the DBSCAN algorithm, written to mirror the Wikipedia
    pseudocode as closely as possible: http://en.wikipedia.org/wiki/DBSCAN
    
    d = Full dataset of point instances
    eps = Maximum search radius
    min_pts = The minimum number of points necessary to qualify a cluster
    """
    def __init__(self, d, eps, min_pts):
        self.d = d
        self.dist = self._euclidean
        self.eps = eps
        self.min_pts = min_pts
        self.assigned = []
        self.cluster = []
    
    def run(self):
        """
        Equivalent to the DBSCAN function in the Wikipedia pseudocode.
        """
        self.assigned = [None for i in self.d]
        self.cluster = []
        # for each unvisited point P in dataset D
        for p in range(0, len(self.d)):
            if not self.assigned[p] == None: continue
            # N = regionQuery(P, eps)
            n = self._getNeighbors(p)
            # if sizeof(N) < MinPts
            if len(n) + 1 < self.min_pts:
                # mark P as NOISE
                self.assigned[p] = -1
            else:
                # C = next cluster
                c = len(self.cluster)
                self.cluster.insert(c, [])
                # expandCluster(P, N, C, eps, MinPts)
                self._expandCluster(p, n, c)
            
    def _getNeighbors(self, p):
        """
        Finds close neighbors based on Euclidean distance (although a different distance
        metric could be subbed in with self.distance).
        """
        neighbors = []
        for i in range(0, len(self.d)):
            if i == p: continue
            if self.dist(p, i) <= self.eps:
                neighbors.append(i)
        return neighbors

    def _expandCluster(self, p, n, c):
        """
        Implementation of the expandCluster portion of DBSCAN, written to mirror
        the Wikipedia pseudocode as closely as possible: http://en.wikipedia.org/wiki/DBSCAN
    
        p = Point instance
        n = Full dataset of Point instances
        c = Cluster number
        """
        # add P to cluster C
        self.cluster[c].append(p)
        self.assigned[p] = c
        p_prime = 0
        # for each point P' in N. Note that because N will change within the loop,
        # we need to use a while loop in Python for this to work properly.
        while p_prime < len(n):
            # if P' is not visited
            if self.assigned[n[p_prime]] == None:
                # N' = regionQuery(P', eps)
                n_prime = self._getNeighbors(n[p_prime])
                # if sizeof(N') >= MinPts
                if len(n_prime) + 1 >= self.min_pts:
                    # N = N joined with N'
                    n += [i for i in n_prime if i not in n]
            # if P' is not yet member of any cluster
            if not (self.assigned[n[p_prime]]) > -1:
                # add P' to cluster C
                self.cluster[c].append(n[p_prime])
                # mark P' as visited
                self.assigned[n[p_prime]] = c
            p_prime += 1

    def _euclidean(self, p1, p2):
        """
        Simple implementation of Euclidean ("as the crow flies") distance for
        judging nearest neighbors. Just be sure the p1 and p2 vectors are the
        same length.
        """
        sum = 0
        for i in range((len(self.d[p1]))):
            sum += (self.d[p1][i] - self.d[p2][i]) ** 2
        return math.sqrt(sum)
        
if __name__ == '__main__':
    inputs = [
        [161.896748456871, 25.0696552938316],
        [124.536306126043, 102.949803235009],
        [23.1287293771747, 60.9901472011115],
        [64.8027076551225, 124.777542503783],
        [61.2784691017587, 124.768467478454],
        [65.8575859381817, 121.369165009353],
        [64.9835283006541, 125.391495652962],
        [65.3726679224055, 121.573309215717],
        [62.7522143330425, 122.272361897398],
        [65.887405679794, 128.306325619109],
        [65.9678300470114, 128.510983631946],
        [62.9840246499516, 130.750667489832],
        [66.870452496456, 129.189951622859],
        [65.6920035600197, 128.22643712],
        [64.0884605033789, 131.145582770929],
        [66.2548200648744, 125.353290710365],
        [68.011933805421, 130.840578845004],
        [67.751343869837, 125.391728902468],
        [64.6913737929426, 127.822012513177],
        [66.8181652582716, 126.145564339589],
        [70.9091390327085, 127.723869043635],
        [64.0655834355857, 124.797499422217],
        [69.9176602754742, 122.914182787528],
        [67.313555957051, 128.509701427538],
        [67.8092960424256, 122.750232404796],
        [64.7418450310361, 123.504969990347],
        [71.2696258078795, 123.495525142411],
        [70.2492955864873, 122.704878813587],
        [67.4411827898584, 120.819619976683],
        [68.5269792457111, 120.221518048318],
        [66.9557912657037, 119.364731973968],
        [63.8331350022927, 122.567011193139],
        [65.1810344927944, 122.954397034133],
        [61.8353881125804, 120.801628043409],
        [66.4504141202197, 121.699558694847],
        [62.530803111149, 123.741077903425],
        [65.4222546878736, 119.94324045768],
        [66.8447473263368, 123.739773968468],
        [106.689987945138, 141.031761131249],
        [105.111987900687, 144.497500277357],
        [104.397357129259, 141.746345218038],
        [105.362714990741, 139.287154732971],
        [107.538317830069, 144.39942372893],
        [104.790206357138, 141.782157530077],
        [103.42935829144, 141.516786448425],
        [105.162052121945, 144.425610898295],
        [105.327825711109, 145.756101884181],
        [102.127010107972, 146.040622171713],
        [102.721377582056, 145.537805374945],
        [105.058624334401, 144.050038267393],
        [105.215858884389, 141.461615909357],
        [105.278999993578, 144.325118740322],
        [105.359756748891, 137.355355139822],
        [104.186807611259, 140.220230876701],
        [108.881976898992, 137.689377445495],
        [101.688395303208, 136.810465359595],
        [104.748574452475, 133.74643562478],
        [102.393046272686, 139.767307486385],
        [101.818202317227, 137.178136984818],
        [140.908947885269, 43.154646466719],
        [139.215561224846, 43.2473453814164],
        [137.996219470166, 40.5679546829779],
        [143.95275133173, 44.0315375882201],
        [138.042031334015, 45.9122374576982],
        [141.714413356502, 39.4675569455139],
        [139.068389034364, 45.8871560562402],
        [140.188288480742, 43.7985208602622],
        [143.934670670191, 42.5785948811099],
        [139.023951004725, 44.9539802400395],
        [140.262683724519, 43.1100534771103],
        [139.418556381715, 41.8949894560501],
        [138.67677817028, 47.2178436270915],
        [138.241288920632, 45.2063152347691],
        [143.67153035407, 43.3959349077195],
        [146.965783149935, 42.1860255228821],
        [140.95998629625, 41.6015680525452],
        [144.310065406142, 41.9430442752782],
        [145.809882230824, 42.16890892433],
        [146.569439372513, 44.9079612342175],
        [140.75571861607, 44.0137354782783],
        [144.17063904088, 42.1429307698272],
        [142.07450964232, 43.3184848739766],
        [147.865109063452, 42.8674810128287],
        [143.93579324591, 41.4222651459277],
        [142.637531774119, 42.8947248656768],
        [142.243334897561, 39.7712499527261],
        [141.51977933757, 45.1264958146494],
        [141.901039240649, 42.947217392968],
        [143.518505709711, 45.7095497918781],
        [139.904611264355, 39.5277482580859],
        [142.501110464102, 41.6896208589897],
        [140.671162643237, 45.3559190970846],
        [141.430685681058, 40.5567031791434],
        [143.088715787511, 41.5071381328162],
        [141.909749050159, 43.6559766873252],
        [139.419220278738, 46.0962324766442],
        [141.595915447688, 46.1465273573995],
        [142.115972748492, 46.2811057593208],
        [139.046542964177, 45.4929149614181],
        [143.478071172023, 40.609769689152],
        [142.719987623394, 43.2983131450601],
        [141.633627854986, 43.2841766730417],
        [143.538992288057, 45.493975085672],
        [139.983389561996, 43.5962452949025],
        [138.131787274498, 42.7234663187992],
        [142.451348749921, 45.0698692107108],
        [144.004803430755, 45.3131371487398],
        [144.077687186422, 43.3384940924589],
        [45.9380275974982, 83.2783805073705],
        [42.2881892991718, 82.5158110694028],
        [48.4480316485278, 86.2748897902202],
        [44.388764315052, 85.9560348237865],
        [48.7638249823358, 81.8093685121275],
        [45.8117200285196, 84.3835120759904],
        [43.7349899848923, 81.2561588690151],
        [45.8312124125659, 85.5578575951513],
        [49.5618889774196, 86.22117973282],
        [49.5253649097867, 84.8105966744479],
        [45.1941606125329, 87.134341398254],
        [46.4607119469438, 87.7279475880787],
        [42.5857547873166, 87.2384601149242],
        [46.4607723217923, 89.0107204280794],
        [42.6088097982574, 81.7370121479035],
        [40.3013752757106, 83.3130952247884],
        [40.5275763240643, 79.2374815687072],
        [45.5839002989233, 83.6340910131112],
        [43.1642628666013, 78.9113502511755],
        [45.8651360790245, 83.5124657382257],
        [43.4795797562692, 84.1240914901718],
        [44.4169631432742, 86.1208110749721],
        [42.7985966913402, 85.6927989486139],
        [41.1684817108326, 84.8232880514115],
        [45.2658742042258, 82.9055543395225],
        [42.3099635227118, 89.0930228193756],
        [43.6495603709482, 87.9082602018025],
        [41.9254609395284, 84.1267267668154],
        [80.4457834165078, 160.462486672215],
        [79.5801961200777, 162.456071352819],
        [77.0065401713364, 158.545959328301],
        [84.0503748403862, 160.230467179557],
        [78.447497616522, 161.902977679623],
        [80.4759590416215, 160.484682564158],
        [77.2733517019078, 158.689318683231],
        [80.3360536887776, 158.641857174924],
        [77.7258890159428, 159.03000803222],
        [83.2912958846427, 158.421969533665],
        [81.2543121050112, 157.335227611708],
        [80.9642110310961, 161.824696439784],
        [83.6369603055064, 159.496689641848],
        [84.1710995095782, 159.234971703729],
        [79.04072470963, 160.93724340573],
        [77.1983139736112, 158.613337269984],
        [76.2658514946233, 161.110131281894],
        [78.9330291021615, 158.426590833114],
        [82.6952174147591, 159.870051636361],
        [78.3199222364929, 158.544640515931],
        [82.4985200264491, 159.380827543559],
        [83.1412990028039, 159.656149322633],
        [81.7786051817238, 162.135952768847],
        [79.6892264124472, 161.09126888169],
        [80.4777704258449, 158.380429318175],
        [84.0137062377762, 159.420392628526],
        [84.8311180160381, 162.522331999382],
        [82.4194227659609, 159.011259640567]
    ]

    a = DBSCAN(inputs, eps=4, min_pts=6)
    a.run()
    print a.cluster
    print a.assigned