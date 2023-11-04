
import math
import random
from sympy import isprime


n = 512
q = 12289
r = 10968 


# n = 4
# q = 7681
# r = 3383 

class NTT:

    # modular expoential algorithm
    # complexity is O(log N)
    def modExponent(self, base, power, M):
        result = 1
        power = int(power)
        base = base % M
        while power > 0:
            if power & 1:
                result = (result * base) % M
            base = (base * base) % M
            power = power >> 1
        return result

    # calculate x^(-1) mod M
    def modInv(self, x, M):
        t, new_t, r, new_r = 0, 1, M, x

        while new_r != 0:
            quotient = int(r / new_r)
            t, new_t = new_t, (t - quotient * new_t)
            r, new_r = new_r, (r % new_r)
        if r > 1:
            return "x is not invertible."
        if t < 0:
            t = t + M
        return t



    def bitReverse(self, num, len):
        """
        integer bit reverse
        input: num, bit length
        output: rev_num 
        example: input 6(110) output 3(011)
        complexity: O(len)
        """
        rev_num = 0
        for i in range(0, len):
            if (num >> i) & 1:
                rev_num |= 1 << (len - 1 - i)
        return rev_num

    def orderReverse(self, poly, N_bit):
        
        for i, coeff in enumerate(poly):
            rev_i = self.bitReverse(i, N_bit)
            if rev_i > i:
                coeff ^= poly[rev_i]
                poly[rev_i] ^= coeff
                coeff ^= poly[rev_i]
                poly[i] = coeff
        return poly

   
    # The complexity is O(N log N)
    def ntt(self, poly, M, N, w):
        """number theoretic transform algorithm"""
        N_bit = N.bit_length() - 1
        rev_poly = self.orderReverse(poly, N_bit)
        for i in range(0, N_bit):
            points1, points2 = [], []
            for j in range(0, int(N / 2)):
                shift_bits = N_bit - 1 - i
                P = (j >> shift_bits) << shift_bits
                 #P becomes the largest multiple of 2^(shift_bits) that is less than or equal to j.
                w_P = self.modExponent(w, P, M)
                odd = poly[2 * j + 1] * w_P
                even = poly[2 * j]
                points1.append((even + odd) % M)
                points2.append((even - odd) % M)
                
                points = points1 + points2
            if i != N_bit:
                poly = points
        return points

 

    def pointwise_multiplication(self,a, b, q):
        """
        Perform point-wise multiplication of two NTT-transformed polynomials
        :param a: first polynomial
        :param b: second polynomial
        :param q: modulus
        :return: point-wise product
        """
        if len(a) != len(b):
            raise ValueError("Input polynomials must have the same length")
        
        return [(a_i * b_i) % q for a_i, b_i in zip(a, b)]
    
   
    # The complexity is O(N log N)
    def intt(self, points, M, N, w):
        """inverse number theoretic transform algorithm"""
        inv_w = self.modInv(w, M)
        inv_N = self.modInv(N, M)
        p = []
        poly = self.ntt(points, M, N, inv_w)
        for i in range(0, N):
            poly[i] = (poly[i] * inv_N) % M
            
        return poly
    





poly1 =  list(map(int, input("Enter coefficients of the first polynomial separated by spaces: ").split()))



poly2 = list(map(int, input("Enter coefficients of the second polynomial separated by spaces: ").split()))

# poly1= [4432,1362,3115,10479,4556,4492,10345,6509,2874,5736,8876,8740,6253,6783,12060,1358,513,5642,3664,2794,5559,9124,1532,5939,9124,7481,5977,9481,9428,9112,1529,5850,2356,11756,1613,11900,4618,2837,5098,6132,4881,3468,4510,2257,1286,3071,8332,2419,91,10706,9422,2268,7719,11128,2933,9635,1978,12103,8690,2957,8203,1433,5680,8360,2563,6456,12135,10133,7398,4223,9757,5567,7492,8133,5168,5261,2681,10357,9018,1193,8657,5307,10198,7995,976,3748,7618,4365,6748,6845,4310,1193,7567,7092,8656,251,5180,10435,5419,1700,6051,957,7568,5664,1002,4745,2163,12238,393,12009,3799,5850,5001,6098,10013,2426,11258,5787,7978,6353,4073,7396,11294,3638,50,11160,2842,3369,8248,5550,11940,11692,8392,12003,2238,10183,7721,7721,4582,11744,6989,7020,11069,8934,3481,6340,2046,2916,6971,2765,10222,10105,2784,10660,10346,3543,3986,3520,3152,11720,6795,1938,1290,1532,1603,3066,2223,6416,11133,8512,11143,7906,1559,4500,204,2409,1641,2018,3420,7855,2441,4590,4632,10225,7332,1566,7740,6749,1181,9044,2074,8896,2401,11011,7780,10536,3147,2930,7868,4903,11000,9025,7699,1852,6189,5960,2080,4196,653,12105,1779,10063,996,3753,1811,7994,7002,3711,9933,9086,1546,411,10731,3159,11098,5788,208,10279,4593,2029,9086,3659,899,4404,4368,8268,6668,2598,1323,1696,1030,9924,4652,5933,8180,7090,9541,4436,7171,7762,10252,10212,8642,1831,2341,11081,6859,4483,10177,4368,3993,1479,11513,5174,523,7679,1708,9273,11858,6051,12120,11869,7341,4309,7538,9468,408,2382,12138,12153,8184,2348,9106,6383,2850,957,10809,7408,9376,8844,1578,3085,1353,1850,8192,10671,1271,4800,5018,12249,12063,6823,7353,2270,2612,12005,2253,2163,3783,11601,2903,899,11369,3026,4528,6495,7722,8811,10994,4392,11735,11493,1423,10632,4071,6241,3918,5504,4757,4845,4791,6450,2496,6533,4910,11572,10096,10342,5123,11958,789,755,2173,4862,3262,11506,7683,11932,1406,10195,1592,5438,6268,3740,8264,11238,11377,41,11302,8006,10366,4580,2200,5371,4054,10259,11009,3094,10539,8387,8608,3799,12122,3342,9199,2218,7167,11173,8871,9071,11864,6300,9046,6556,6540,4105,4767,8594,7079,6956,10023,11397,5156,11217,8032,11839,11236,2426,8459,119,1555,8449,5047,3893,2573,2670,1626,10953,1610,9892,4769,11231,8481,2702,6626,10976,831,2628,12065,7876,1850,5430,5029,5710,2770,7262,9718,8415,5496,2470,12042,714,6784,9711,7494,2538,8230,7984,12011,9768,1663,5110,11768,8645,10844,11411,11599,6291,583,5632,11956,10974,6968,9339,665,1440,3367,5393,4284,4147,1111,11050,4105,3449,10895,1503,7880,6122,4811,3462,6915,4688,1862,8187,11895,3767,3681,12086,2660,10151,1061,2611,11790,10724,820,10765,6580,624,6197,4922,6637,9033,3435,8609,8643,12239,4673,11572,9126,12121,8554,4296,11465,4705,5696,11163,1068,4694,6835,11176,9749,3954]

# poly2= [3875,7449,9619,4183,6575,11949,695,5099,6749,9215,10857,8114,8962,8119,6735,1019,12060,190,12122,3494,10024,11911,11221,7163,11222,3736,10515,1741,3487,3256,444,5521,132,6721,3834,1332,7476,1897,7026,2408,2266,2293,4776,278,2341,7953,6648,7688,715,3656,11831,1680,7887,6942,4938,10344,6668,9771,8517,4340,8438,1684,9141,84,521,9359,2967,7035,1160,11974,11346,7266,4766,7807,2200,1279,8627,8181,11373,7655,11431,786,2145,6446,5163,9858,4883,11272,339,11415,3000,10070,2353,10071,9565,2809,6937,3466,3256,4741,9215,10981,4819,9594,9858,2432,5301,9839,8783,1748,7553,6541,9693,10363,9195,6096,1977,3120,10117,11186,4371,12053,5824,6534,7078,6889,6998,11508,10176,11481,7281,3661,9752,4943,6106,7986,10498,3918,1671,1867,8124,118,9837,5591,2803,11023,2179,4415,5028,11072,310,8664,466,799,11281,3694,2435,451,7052,5603,8879,772,1505,2600,7520,70,3284,10465,11295,9068,10536,12184,306,1638,9531,1337,1274,5398,3938,5100,5574,6024,1794,2434,6556,7979,46,9793,6633,1400,9726,5020,8451,6939,11948,11470,11657,7506,3525,1323,2500,1628,8096,3334,1476,6147,7196,7181,7183,8267,11137,5665,1325,1015,9665,5903,2343,5946,9248,2754,1746,5031,10394,4780,9896,8926,10993,5976,7126,9546,620,8939,8999,7900,4035,2690,12022,9519,1182,2426,2807,5782,906,3506,10527,8143,7507,12093,3772,172,3370,8982,7940,2906,984,1361,4018,8563,198,9135,11033,2818,389,212,340,7093,6899,11506,6045,5389,219,5663,346,5410,3686,1625,3981,3553,1748,8188,3513,5031,4210,9758,812,11592,8393,521,10941,3314,98,9988,1434,10613,8639,162,7260,4943,7258,3435,11949,8473,10774,12182,1295,12200,4390,7960,2003,11999,3001,5872,6629,11092,3667,7004,7709,159,9218,404,9013,5607,5958,5115,6437,5707,6961,9370,10812,8613,5020,4647,8472,1778,8638,8461,2620,11657,577,9042,3778,10726,7811,1027,10625,7746,3254,8294,1097,8282,260,4848,2536,10726,10884,357,1224,11436,3170,5959,8338,379,5172,2798,8579,1176,8872,4390,588,896,8571,4565,8816,2877,8153,7046,10250,8578,6847,6780,9442,7256,9674,5743,4156,2798,11754,10639,8378,12258,5695,4874,10308,3531,2180,3204,4209,2005,259,3851,10426,5737,9836,5827,11027,4574,4127,11833,7077,1903,2452,4574,7665,10409,7002,8143,8629,9078,4667,8183,1220,9280,1580,1803,1721,1074,8517,9494,4788,5042,5146,10052,9216,7962,3570,7470,5858,9101,4879,4941,8406,7867,5761,8933,4543,7646,4902,10593,1229,9375,5721,1218,11860,7346,7829,7479,11816,612,2191,3659,2506,6008,8357,2549,1027,11370,5959,9978,269,3354,9670,4003,7862,3227,2086,595,2115,10787,1525,3573,1138,12282,5482,611,7276,9658,7744,2816,10855,1101,8234,5995,301,4806,6779,1157,401,7862,7517,7433,12268,5118,10212,10590,9397,3500,4110,6447,8819,9348,1863,9325]
# Pad the coefficients array with zeros to the length n
poly1 += [0] * (n - len(poly1))
poly2 += [0] * (n - len(poly2))


ntt_instance=NTT()

ntt_poly1= ntt_instance.ntt(poly1,q,n,r)
ntt_poly2= ntt_instance.ntt(poly2,q,n,r)


# inv_ntt_poly1=ntt_instance.intt(ntt_poly1,q,n,r)

# inv_ntt_poly2=ntt_instance.intt(ntt_poly2,q,n,r)

product_ntt = ntt_instance.pointwise_multiplication(ntt_poly1, ntt_poly2, q)

intt_result=ntt_instance.intt(product_ntt,q,n,r)







# print("NTT poly1:", ntt_poly1)
# print("Inverse NTT poly1:", inv_ntt_poly1)

# print("NTT poly2:", ntt_poly2)
# print("Inverse NTT poly2:", inv_ntt_poly2)

# product_ntt_2 = ntt_instance.pointwise_multiplication(inv_ntt_poly1, inv_ntt_poly2, q)
# print("product_ntt_2:", product_ntt_2)

# Output the result
# print("NTT result:", ntt_result)
print("Inverse NTT result:", intt_result)


