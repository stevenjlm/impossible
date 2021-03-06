#include <iostream>

using namespace std;

void say_hello(const char* name, const char* other_name) {
    cout << "Hello " <<  name << "!\n";
    cout << "Goodbye " << other_name << "!\n";
}

#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
using namespace boost::python;

BOOST_PYTHON_MODULE(hello)
{
    def("say_hello", say_hello);
}
