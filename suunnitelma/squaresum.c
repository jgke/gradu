int sum_square_difference(int n) {
    int i, sum, square_sum;
    for(i = 1; i <= n; i++) {
        sum += i;
        square_sum += i*i;
    }
    sum *= sum;
    return sum - square_sum;
}
