def solution(area):
    def get_max_square(num):
        return max([x * x for x in range(1, num + 1) if x * x <= num])

    _area = area
    return_list = []

    while(_area > 0):
        max_sq = get_max_square(_area)
        return_list.append(max_sq)
        _area -= max_sq

    return return_list


if __name__ == '__main__':
    print(solution(12))
    print(solution(15324))
