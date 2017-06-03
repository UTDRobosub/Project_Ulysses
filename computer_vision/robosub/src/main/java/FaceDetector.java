import org.opencv.core.*;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;

import java.net.URL;

public class FaceDetector {

    public static final String FACIAL_RECOGNITION_CLASSIFIER = "classifiers/haarcascade_frontalface_default.xml";

    public Mat detect(Mat frame) {

        URL resource = getClass().getClassLoader().getResource(FACIAL_RECOGNITION_CLASSIFIER);

        if (resource == null) {
            System.out.println("Could not find classifier!");
            return null;
        }

        CascadeClassifier faceDetector = new CascadeClassifier(resource.getPath().substring(1));

        MatOfRect faceDetections = new MatOfRect();
        faceDetector.detectMultiScale(frame, faceDetections);

        System.out.println(String.format("Detected %s faces", faceDetections.toArray().length));

        for (Rect rect : faceDetections.toArray()) {
            Imgproc.rectangle(frame, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y + rect.height),
                    new Scalar(0, 255, 0));
        }

        return frame;
    }
}