
train:
	# train p5 models
	#python train.py --workers 8 --device cpu --batch-size 4 --data data/coco.yaml --img 640 640 --cfg cfg/training/yolov7.yaml --weights '' --name yolov7 --hyp data/hyp.scratch.p5.yaml
	#python train.py --workers 0 --device cpu --batch-size 4 --data data/coco.yaml --img 640 640 --cfg cfg/training/yolov7-tiny.yaml --weights '' --name yolov7-tiny --hyp data/hyp.scratch.tiny.yaml
	python train.py --workers 0 --device cpu --batch-size 4 --data data/cdla.yaml --img 640 640 --cfg cfg/training/yolov7-tiny.yaml --weights '' --name yolov7-tiny --hyp data/hyp.scratch.tiny.yaml

#	# train p6 models
#	python train_aux.py --workers 8 --device 0 --batch-size 16 --data data/coco.yaml --img 1280 1280 --cfg cfg/training/yolov7-w6.yaml --weights '' --name yolov7-w6 --hyp data/hyp.scratch.p6.yaml

detect:
	python detect.py --weights yolov7-tiny.pt --conf 0.25 --img-size 640 --source inference/images/horses.jpg

.PHONY: train detect
