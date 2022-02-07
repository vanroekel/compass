import numpy as np


def flood_fill(thk, vx, vy):
    """
    Remove glaciers and ice-fields that are not connected to the ice sheet.

    Parameters
    ----------
    thk : numpy.ndarray
        Ice thickness from gridded dataset
    vx : numpy.ndarry
        Velocity x-component from gridded dataset
    vy : numpy.ndarray
        Velocity y-component from gridded dataset

    Returns
    -------
    thkTrimmed : numpy.ndarray
        Ice thickness after flood-fill is applied
    vxTrimmed : numpy.ndarray
        Velocity x-component after flood-fill is applied
    vyTrimmed : numpy.ndarry
        Velocity y-component after flood-fill is applied
    """
    sz = thk.shape
    searchedMask = np.zeros(sz)
    floodMask = np.zeros(sz)
    iStart = sz[0] // 2
    jStart = sz[1] // 2
    floodMask[iStart, jStart] = 1

    neighbors = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])

    lastSearchList = np.ravel_multi_index([[iStart], [jStart]],
                                          sz, order='F')

    cnt = 0
    while len(lastSearchList) > 0:
        cnt += 1
        newSearchList = np.array([], dtype='i')

        for iii in range(len(lastSearchList)):
            [i, j] = np.unravel_index(lastSearchList[iii], sz, order='F')
            # search neighbors
            for n in neighbors:
                ii = i + n[0]
                jj = j + n[1]  # subscripts to neighbor
                # only consider unsearched neighbors
                if searchedMask[ii, jj] == 0:
                    searchedMask[ii, jj] = 1  # mark as searched

                    if thk[ii, jj] > 0.0:
                        floodMask[ii, jj] = 1  # mark as ice
                        # add to list of newly found  cells
                        newSearchList = np.append(newSearchList,
                                                  np.ravel_multi_index(
                                                      [[ii], [jj]], sz,
                                                      order='F')[0])
        lastSearchList = newSearchList

    # apply flood fill
    thkTrimmed = thk.copy()
    vxTrimmed = vx.copy()
    vyTrimmed = vy.copy()

    thkTrimmed[floodMask == 0] = 0.0
    vxTrimmed[floodMask == 0] = 0.0
    vyTrimmed[floodMask == 0] = 0.0

    return thkTrimmed, vxTrimmed, vyTrimmed
