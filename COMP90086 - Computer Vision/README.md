# COMP90086 - Computer Vision

### Assignment 1 - Laplacian Pyramid Image Compression
Python implementations of Laplacian pyramid construction and reconstruction functions were utilized to compress images. This involved quantizing pyramid layers and subsequently reconstructing the image. The impact of compression on image quality and frequency content was thoroughly assessed, leading to the identification of an optimal trade-off between compression ratio and reconstruction error.

----

### Assignment 2 - Scene Classification with CNNs
A CNN was implemented and trained on a subset of the SceneNet dataset. Data augmentation techniques were applied to enhance the dataset, and the performance of the trained model was analyzed. The influence of different convolutional kernel sizes on accuracy was examined, and the learned kernels were visualized. 

----

### Assignment 3 - Image Inpainting
A thorough analysis was conducted on an image inpainting algorithm designed to fill in missing regions in images by replicating patterns from neighboring areas. Various enhancements were explored to improve the image quality, including experimenting with different context window sizes and shapes. Additionally, alternative patch similarity metrics, sampling approaches, and reconstruction orders were tested to optimize the inpainting process.

----

### Final Project - Visually Similar Image Matching
Models were developed and assessed for the purpose of matching similar image pairs from the Totally-Looks-Like dataset. Various techniques were explored, including Canny edge detection, utilization of pre-trained networks, and the implementation of a Siamese network with triplet loss. Among these approaches, the fine-tuned Siamese network exhibited superior performance, making it the most effective method for the task at hand.