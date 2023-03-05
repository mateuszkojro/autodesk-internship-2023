/*

There is a 3D point and a line segment (bounded 3D line) given by endpoints.
Write a method that will compute the distance from the point to the segment.
Consider all possible locations of the point in relation to the segment.
Handle all boundary cases.

All vector operations are available from included Eigen library.
Documentation: https://eigen.tuxfamily.org/dox/group__QuickRefPage.html

*/

#include <Eigen/Core>
#include <Eigen/Geometry>

using Eigen::Vector3d;

// https://eigen.tuxfamily.org/dox/group__QuickRefPage.html

// Method calculates a distance from point p to segment ab
// a - coordinates of the first point of the segment
// b - coordinates of the second point of the segment
// p - coordinates of the point to calculate distance to the segment from
// Returns distance
double Distance(const Vector3d &a, const Vector3d &b, const Vector3d &p) {
    // ************* YOUR CODE HERE *************

    // Change the coordinate system, so we are in the reference frame where `a = (0,0)`
    Vector3d ab = b - a;
    Vector3d ap = p - a;

    // If `ap` and `ab` point in different directions (`ap` is "lagging" behind `ab`) (`ap * ab` < 0) or `ap` and `ab`
    // are perpendicular (`ap * ab` = 0)
    // the shortest distance is just the distance between `a` and `p` so just `sqrt((p-a)**2)`
    if (ap.dot(ab) <= 0.0) {
        return ap.norm();
    }

    Vector3d bp = p - b;

    // If `bp` is pointing in the same direction as `ab` (`bp` is "in front of" `ab`) or `bp` and `ab` are perpendicular
    // the distance is just the distance between `b` and `p`
    if (bp.dot(ab) >= 0.0) {
        return bp.norm();
    }

    // If `p` "lays between" 'a' and `b` the shortest distance between `ab` and `p` is a segment (`d`) starting at `p`
    // that is perpendicular to `ab`
    // This segment `d` would be equivalent to the height of a parallelogram (`h`) with sides `ab` and `ap`
    // and the area (`A`) of it could be obtained using the properties of the cross product - namely:
    // `A` = abs(`ab` x `ap`)
    // and using the standard equation for the area of a parallelogram:
    // `A` = `h` * abs(`ab`)
    // which means that we can get:
    // `d` = `h` = abs(`ab` x `ap`) / abs(`ab`)
    return ab.cross(ap).norm() / ab.norm();
    // ******************************************
}

#include <iostream>

using namespace std;

int main() {

    // This is only simple example.
    // Solution must handle all cases.

    Vector3d a(0, 0, 0), b(1, 0, 0), p(1, 1, 0);
    cout << "Distance = " << Distance(a, b, p) << endl;
    return 0;
}
