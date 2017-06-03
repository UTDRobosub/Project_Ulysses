import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.videoio.VideoCapture;

import javax.swing.*;
import java.awt.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.image.BufferStrategy;
import java.awt.image.BufferedImage;
import java.awt.image.DataBufferByte;

public class Main {

    static {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    }

    public static void main(String[] args) {

        final VideoCapture camera = new VideoCapture(0);

        if (!camera.isOpened()) {
            System.out.println("Camera Error");
        } else {
            System.out.println("Camera OK?");
        }

        // Open JFrame
        final String title = "Test Window";
        final int width = 1200;
        final int height = width / 16 * 9;

        // Create the frame
        final JFrame frame = new JFrame(title);

        frame.setSize(width, height);
        frame.setLocationRelativeTo(null);
        frame.setResizable(false);
        frame.setVisible(true);

        // Create the canvas
        Canvas canvas = new Canvas();

        canvas.setSize(width, height);
        canvas.setBackground(Color.BLACK);
        canvas.setVisible(true);
        canvas.setFocusable(false);

        frame.add(canvas);
        canvas.createBufferStrategy(3);

        frame.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent we) {
                camera.release();
                System.exit(0);
            }
        });

        boolean running = true;

        BufferStrategy bufferStrategy;
        Graphics graphics;

        while (running) {
            bufferStrategy = canvas.getBufferStrategy();
            graphics = bufferStrategy.getDrawGraphics();
            graphics.clearRect(0, 0, width, height);

            Mat image = new Mat();

            camera.read(image);

            FaceDetector faceDetector = new FaceDetector();
            Mat scanned = faceDetector.detect(image);

            graphics.drawImage(matToBufferedImage(scanned), 0, 0, null);

            bufferStrategy.show();
            graphics.dispose();
        }
    }

    private static BufferedImage matToBufferedImage(Mat m){
        int type = BufferedImage.TYPE_BYTE_GRAY;
        if ( m.channels() > 1 ) {
            type = BufferedImage.TYPE_3BYTE_BGR;
        }
        int bufferSize = m.channels()*m.cols()*m.rows();
        byte [] b = new byte[bufferSize];
        m.get(0,0,b);
        BufferedImage image = new BufferedImage(m.cols(),m.rows(), type);
        final byte[] targetPixels = ((DataBufferByte) image.getRaster().getDataBuffer()).getData();
        System.arraycopy(b, 0, targetPixels, 0, b.length);
        return image;
    }
}
