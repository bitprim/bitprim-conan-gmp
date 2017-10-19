import platform
from conan.packager import ConanMultiPackager
import os
import cpuid
import copy

if __name__ == "__main__":

    # print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    # print(cpuid.cpu_vendor())
    # print(cpuid.cpu_name())
    # print(cpuid.cpu_microarchitecture())
    # print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

    builder = ConanMultiPackager(username="bitprim", channel="stable",
                                 remotes="https://api.bintray.com/conan/bitprim/bitprim")
    builder.add_common_builds(shared_option_name="gmp:shared", pure_c=True)
    builder.password = os.getenv("CONAN_PASSWORD")

    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        if settings["build_type"] == "Release" \
                and settings["arch"] == "x86_64" \
                and not ("gmp:shared" in options and options["gmp:shared"]):
            
            opt1 = copy.deepcopy(options)
            opt2 = copy.deepcopy(options)
            opt3 = copy.deepcopy(options)
            opt4 = copy.deepcopy(options)

            opt1["gmp:microarchitecture"] = "x86_64"
            opt2["gmp:microarchitecture"] = ''.join(cpuid.cpu_microarchitecture())
            opt3["gmp:microarchitecture"] = "haswell"
            opt4["gmp:microarchitecture"] = "skylake"

            filtered_builds.append([settings, opt1, env_vars, build_requires])
            filtered_builds.append([settings, opt2, env_vars, build_requires])
            filtered_builds.append([settings, opt3, env_vars, build_requires])
            filtered_builds.append([settings, opt4, env_vars, build_requires])

    builder.builds = filtered_builds

    builder.run()
