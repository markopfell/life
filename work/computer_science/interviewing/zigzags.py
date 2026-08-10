def solution(numbers):
    zigzags = []
    
    for i, _ in enumerate(numbers):
        print(i)
        if i + 2 >= len(numbers)  or i + 1 >= len(numbers):
            print(i)
        else:
            a = numbers[i]
            b = numbers[i + 1]
            c = numbers[i + 2] 
            if (a < b and b > c) or (a > b and b < c):
                zigzags.append(1)
            else:
                zigzags.append(0)
    return zigzags

print(solution([1,2,1,3,4]))