## Rock Particle Segmentation 


#### How does segmentation algorithm look like?
1. Reduce Noise by removing left and right side of image
    1. Get contours using canny detector
    2. Dilate to preserve regions with fragments
    3. Erode image so that noisy areas are removed
2. Separate background from foreground
    1. morphological opening (erosion followed by a dilation using the same structuring element for both operations)
    2. additional dilation and buffer for background
    3. use distance transform operator to get regions surrounded by black edges
    4. use distance transform as base for thresholding to get foreground buffer
3. Create markers based on received foreground buffer
4. Use watershed algorithm to separate regions
    
 
#### Requirments
- Python >=3.5
- matplotlib (generate histograms)
- opencv

#### How to run script? 

`pip install -r requirements.txt`

`python rock_segmentation.py --input /folder/with/original/images --output /store/output/here`