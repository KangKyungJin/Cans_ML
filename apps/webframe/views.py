from django.shortcuts import render, redirect
from .models import photos, imageDetect
import os, sys
import cv2
import numpy as np
import tensorflow.compat.v1 as tf
from .utils import label_map_util
from .utils import visualization_utils as vis_util
# Fixed live detection
from django.http.response import StreamingHttpResponse
from PIL import Image
from django.contrib import messages
from tensorflow import keras
import base64

def homepage(request):
    return render(request, 'webframe/homepage.html')

def image(request):
    images = photos.objects.last()
    context = {
        'images' : images
    }
    return render(request, 'webframe/image.html', context)

def webcam(request):
    return render(request, 'webframe/webcam.html')

def upload(request):
    image = request.FILES['img']
    print(image, "stop")
    errors = photos.objects.validator(request.FILES)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/images')
    else: 
        
        request.session['name']= str(request.FILES['img'])
        photos.objects.create(img = image)
        return redirect('/ml_process')

def ml_image(request):
    image_name = "ml" + request.session['name']
    context = {
        'name' : image_name,
    }
    return render(request, 'webframe/ml_image.html', context)

# Fixed live detection
def video_feed(request):
    return StreamingHttpResponse(live_feed(), content_type='multipart/x-mixed-replace; boundary=frame')

sys.path.append("..")
def ml_process(request):
    # Name of the directory containing the object detection module we're using
    MODEL_NAME = 'inference_graph'
    IMAGE_NAME = request.session['name']

    # Grab path to current working directory
    CWD_PATH = os.getcwd()

    # Path to frozen detection graph .pb file, which contains the model that is used
    # for object detection.
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

    # Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

    # Path to image
    PATH_TO_IMAGE = os.path.join(CWD_PATH, 'media', IMAGE_NAME)

    # Path to write
    PATH_TO_WRITE = os.path.join(CWD_PATH, 'apps/webframe/static/webframe/images', "ml"+IMAGE_NAME)
    print(PATH_TO_WRITE + "|" * 80)


    # Number of classes the object detector can identify
    NUM_CLASSES = 3

    # Load the label map.
    # Label maps map indices to category names, so that when our convolution
    # network predicts `5`, we know that this corresponds to `king`.
    # Here we use internal utility functions, but anything that returns a
    # dictionary mapping integers to appropriate string labels would be fine
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Load the Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    # Define input and output tensors (i.e. data) for the object detection classifier

    # Input tensor is the image
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    # Number of objects detected
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Load image using OpenCV and
    # expand image dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value
    image = cv2.imread(PATH_TO_IMAGE)
    image_expanded = np.expand_dims(image, axis=0)

    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})

    # Draw the results of the detection (aka 'visulaize the results')

    vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.60)

    # All the results have been drawn on image. Now display the image.
    # cv2.imshow('Object detector', image)
    cv2.imwrite(PATH_TO_WRITE, image)

    return redirect('/ml_image')

# Fixed live detection
def live_feed():
    MODEL_NAME = 'inference_graph'

    # Grab path to current working directory
    CWD_PATH = os.getcwd()

    # Path to frozen detection graph .pb file, which contains the model that is used
    # for object detection.
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

    # Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

    # Number of classes the object detector can identify
    NUM_CLASSES = 3

    ## Load the label map.
    # Label maps map indices to category names, so that when our convolution
    # network predicts `5`, we know that this corresponds to `king`.
    # Here we use internal utility functions, but anything that returns a
    # dictionary mapping integers to appropriate string labels would be fine
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Load the Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)


    # Define input and output tensors (i.e. data) for the object detection classifier

    # Input tensor is the image
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    # Number of objects detected
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Initialize webcam feed
    video = cv2.VideoCapture(0)
    ret = video.set(3,1280)
    ret = video.set(4,720)

    while(True):

        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        ret, frame = video.read()
        frame_expanded = np.expand_dims(frame, axis=0)

        # Perform the actual detection by running the model with the image as input
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})

        # Draw the results of the detection (aka 'visulaize the results')
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.60)

        # All the results have been drawn on the frame, so it's time to display it.
        # cv2.imshow('Object detector', frame)
        cv2.imwrite('demo.jpg', frame)
        yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')