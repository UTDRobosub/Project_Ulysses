#ifndef ROBOTMOTOR_H
#define ROBOTMOTOR_H

/*3/16/2017
The following functions need to be made: moveForward(), moveBack(), turnLeft(),
turnRight(), strafeLeft(), strafeRight() using the turnMotors() function in the
arduino recent test sketch. If we could make class for these functions that would be
ideal. It would be helpful for us later, when using beaglebone. please use C/C++.

We also need to make a generic PID class, I will upload an example to within the
libraries folder. If you would like to more info an PID loops please go the Follow
website: (http://brettbeauregard.com/blog/2012/01/arduino-pid-autotune-library/).
If you find better resource for this, please share it with me (text it to me).

Sonar senors stuff is coming soon, so please do some research into digital signal processing.*/

class Motor
{
    public:
        void moveForward(int,int);
        void moveBack(int,int);
        void turnLeft(int,int);
        void turnRight(int,int);
        void strafeLeft(int,int);
        void strafeRight(int,int);
        void turnMotors(int,int);
    private:
};

#endif // CONTROLLER_H
