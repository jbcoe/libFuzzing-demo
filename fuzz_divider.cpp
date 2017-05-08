#include <cstdint>
#include <cstddef>
#include <cassert>

int divide(int x, int y) {
  if (x > 10 || x < -10)
    return -1;
  if (y > 10 || y < -10)
    return -1;
  if (y == 0)
    return -1;

  assert(x!=3);
  
  return x / y; 
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  if(size != 2*sizeof(int)) return 0;

  auto input = reinterpret_cast<const int *>(data);
  volatile auto r = divide(input[0], input[1]);

  return 0;
}

