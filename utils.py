def cluster(data, maxgap, key=lambda x: x):
    '''Arrange data into groups where successive elements
       differ by no more than *maxgap*

        >>> cluster([1, 6, 9, 100, 102, 105, 109, 134, 139], maxgap=10)
        [[1, 6, 9], [100, 102, 105, 109], [134, 139]]

        >>> cluster([1, 6, 9, 99, 100, 102, 105, 134, 139, 141], maxgap=10)
        [[1, 6, 9], [99, 100, 102, 105], [134, 139, 141]]

    '''
    data.sort(key=key)
    groups = [[data[0]]]
    for x in data[1:]:
        if abs(key(x) - key(groups[-1][-1])) <= maxgap:
            groups[-1].append(x)
        else:
            groups.append([x])
    return groups
