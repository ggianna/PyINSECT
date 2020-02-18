#!/usr/bin/env python
import pdb
import sys
# sys.path.append('..')
from source import NGramGraphCollector

ngc = NGramGraphCollector()
print("Adding texts...")
ngc.addText("A test...")
ngc.addText("Another, bigger test. But a test, anyway...")
print("Adding texts... Done!")

print("Getting appropriateness...")
print((ngc.getAppropriateness("A test...")))
print((ngc.getAppropriateness("Another, bigger test...")))
print((ngc.getAppropriateness("Something irrelevant!")))
print("Getting appropriateness... Done!")
