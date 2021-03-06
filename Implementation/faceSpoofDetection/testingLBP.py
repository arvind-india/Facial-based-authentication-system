from __future__ import print_function

import cv2
import matplotlib.pyplot as plt

import features
import openface

P = 8
R = 2

mlbp = features.MultiScaleLocalBinaryPatterns((8, 1), (24, 3),(40, 5))
#mlbp = features.LocalBinaryPatterns(P, R)

faceImg = cv2.imread('../data/face2.jpg', cv2.IMREAD_COLOR)
spoofFaceImg = cv2.imread('../data/spoofFace2.jpg', cv2.IMREAD_COLOR)

faceImg = cv2.cvtColor(faceImg, cv2.COLOR_BGR2RGB)
spoofFaceImg = cv2.cvtColor(spoofFaceImg, cv2.COLOR_BGR2RGB)

'''
start = time.time()

faceLBPHist = mlbp.computeFeature(cv2.cvtColor(faceImg, cv2.COLOR_RGB2GRAY))

print('Computing the lbp feature of the real face took {}'.format(time.time()-start))

start = time.time()
fastFaceLBPHist = mlbp.computeFeatureFaster(cv2.cvtColor(spoofFaceImg, cv2.COLOR_RGB2GRAY))
print('Computing the lbp feature in the fast way took {}'.format(time.time() - start))

fastFaceLBPHist = map(lambda x:-x, fastFaceLBPHist)
diff = np.add(faceLBPHist, fastFaceLBPHist)
diff = np.absolute(diff)

print(sum(diff))
'''


align = openface.AlignDlib("/home/doru/Desktop/Licenta/Implementation/models/dlib/shape_predictor_68_face_landmarks"
                           ".dat")

# Get all bounding boxes
bb = align.getAllFaceBoundingBoxes(faceImg)
bbs = align.getAllFaceBoundingBoxes(spoofFaceImg)

if bb is None or bbs is None:
    raise Exception("No faces detected")


alignedFaces = []

for box in bb:
    alignedFaces.append(align.align(
            260,
            faceImg,
            box,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE))

if alignedFaces is None:
        raise Exception("Unable to align the frame")

alignedSpoofFaces = []
for box in bbs:
    alignedSpoofFaces.append(align.align(
        260,
        spoofFaceImg,
        box,
        landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE
    ))

if alignedSpoofFaces is None:
        raise Exception("Unable to align the frame")

realImgRedChannel = alignedFaces[0][:, :, 2]
spoofImgRedChannel = alignedSpoofFaces[0][:, :, 2]

if isinstance(mlbp, features.LocalBinaryPatterns):
    hist, bins, lbpFV = mlbp.compute(realImgRedChannel)
    bins = bins.astype('float')
    bins = bins + (bins[1] - bins[0])/2

    histSpoof, binsSpoof, lbpFVSpoof = mlbp.compute(spoofImgRedChannel)
    binsSpoof = binsSpoof.astype('float')
    binsSpoof = binsSpoof + (binsSpoof[1] - binsSpoof[0])/2

    f, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(nrows=3, ncols=2, figsize=(9,6))

    ax1.imshow(alignedFaces[0])
    ax3.bar(bins[:-1], hist)
    ax5.hist(lbpFV.ravel(), normed=True)


    ax2.imshow(alignedSpoofFaces[0])
    ax4.bar(binsSpoof[:-1], histSpoof)
    ax6.hist(lbpFVSpoof.ravel(), normed=True)



    print(lbpFV.shape)

    plt.show()

    lbpFV = lbpFV.astype('uint8')
    cv2.imshow('lbp', lbpFV)

    lbpFVSpoof = lbpFVSpoof.astype('uint8')
    cv2.imshow('lbpspoof', lbpFVSpoof)
    while(1):
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
else:
    hist = mlbp.compute(realImgRedChannel)
    histSpoof = mlbp.compute(spoofImgRedChannel)

    print(len(hist))
    print(len(histSpoof))


