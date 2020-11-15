def solution(total_lambs):
    """Return the difference between the maximum and minimum possible henchman.

    The length of the returned arrays is equal to the amount of henchman
    employed for that condition. Subtract the length of the generous array
    from the stingy array.
    """
    a = len(get_generous_result(total_lambs))
    b = len(get_stingy_result(total_lambs))

    print(b - a)
    return b - a


def get_stingy_result(lambs):
    """Calculates the most stingy result as a list of LAMB payments.

    The most stingy result is to make sure that the sum of the payments to the
    next two subordinate henchman is equal to their senior. This satisfies
    condition 3 on the README file whilst using the least amount of LAMBS.
    Essentially this gives the fibonacci sequence.
    """
    sti_result = []
    this_payment = 1
    while(sum(sti_result) <= lambs):
        sti_result.append(this_payment)
        if(len(sti_result) > 1):
            this_payment = sum(sti_result[-2:])

    return sti_result


def get_generous_result(lambs):
    """Calculates most generous result as a list of LAMB payments.

    The most generous case is to pay every new senior henchman double the
    amount of LAMBS as their subordinate. Keep appending payments that double
    until the total amount of lambs used is more than the amount available.
    """
    # Gives 2*n sequence
    gen_result = []
    this_payment = 1
    while(sum(gen_result) <= lambs):
        gen_result.append(this_payment)
        this_payment *= 2

    return gen_result


if __name__ == '__main__':
    solution(10)
    solution(143)
