#include <cstdio>
#include <openvdb/openvdb.h>

int main(int argc, char *argv[])
{
    openvdb::initialize();
    openvdb::uninitialize();
    puts("Test successful\n");
    return 0;
}
