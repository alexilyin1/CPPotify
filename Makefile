# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.19

# Default target executed when no arguments are given to make.
default_target: all

.PHONY : default_target

# Allow only one "make -f Makefile2" at a time, but pass parallelism.
.NOTPARALLEL:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /snap/cmake/805/bin/cmake

# The command to remove a file.
RM = /snap/cmake/805/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/amt99/Desktop/CPPotify_save

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/amt99/Desktop/CPPotify_save

#=============================================================================
# Targets provided globally by CMake.

# Special rule for the target rebuild_cache
rebuild_cache:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Running CMake to regenerate build system..."
	/snap/cmake/805/bin/cmake --regenerate-during-build -S$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR)
.PHONY : rebuild_cache

# Special rule for the target rebuild_cache
rebuild_cache/fast: rebuild_cache

.PHONY : rebuild_cache/fast

# Special rule for the target edit_cache
edit_cache:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Running CMake cache editor..."
	/snap/cmake/805/bin/ccmake -S$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR)
.PHONY : edit_cache

# Special rule for the target edit_cache
edit_cache/fast: edit_cache

.PHONY : edit_cache/fast

# The main all target
all: cmake_check_build_system
	$(CMAKE_COMMAND) -E cmake_progress_start /home/amt99/Desktop/CPPotify_save/CMakeFiles /home/amt99/Desktop/CPPotify_save//CMakeFiles/progress.marks
	$(MAKE) $(MAKESILENT) -f CMakeFiles/Makefile2 all
	$(CMAKE_COMMAND) -E cmake_progress_start /home/amt99/Desktop/CPPotify_save/CMakeFiles 0
.PHONY : all

# The main clean target
clean:
	$(MAKE) $(MAKESILENT) -f CMakeFiles/Makefile2 clean
.PHONY : clean

# The main clean target
clean/fast: clean

.PHONY : clean/fast

# Prepare targets for installation.
preinstall: all
	$(MAKE) $(MAKESILENT) -f CMakeFiles/Makefile2 preinstall
.PHONY : preinstall

# Prepare targets for installation.
preinstall/fast:
	$(MAKE) $(MAKESILENT) -f CMakeFiles/Makefile2 preinstall
.PHONY : preinstall/fast

# clear depends
depend:
	$(CMAKE_COMMAND) -S$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR) --check-build-system CMakeFiles/Makefile.cmake 1
.PHONY : depend

#=============================================================================
# Target rules for targets named pybind11module

# Build rule for target.
pybind11module: cmake_check_build_system
	$(MAKE) $(MAKESILENT) -f CMakeFiles/Makefile2 pybind11module
.PHONY : pybind11module

# fast build rule for target.
pybind11module/fast:
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11module.dir/build.make CMakeFiles/pybind11module.dir/build
.PHONY : pybind11module/fast

#=============================================================================
# Target rules for targets named pybind11app

# Build rule for target.
pybind11app: cmake_check_build_system
	$(MAKE) $(MAKESILENT) -f CMakeFiles/Makefile2 pybind11app
.PHONY : pybind11app

# fast build rule for target.
pybind11app/fast:
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11app.dir/build.make CMakeFiles/pybind11app.dir/build
.PHONY : pybind11app/fast

source/app/app.o: source/app/app.cpp.o

.PHONY : source/app/app.o

# target to build an object file
source/app/app.cpp.o:
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11app.dir/build.make CMakeFiles/pybind11app.dir/source/app/app.cpp.o
.PHONY : source/app/app.cpp.o

source/app/app.i: source/app/app.cpp.i

.PHONY : source/app/app.i

# target to preprocess a source file
source/app/app.cpp.i:
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11app.dir/build.make CMakeFiles/pybind11app.dir/source/app/app.cpp.i
.PHONY : source/app/app.cpp.i

source/app/app.s: source/app/app.cpp.s

.PHONY : source/app/app.s

# target to generate assembly for a file
source/app/app.cpp.s:
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11app.dir/build.make CMakeFiles/pybind11app.dir/source/app/app.cpp.s
.PHONY : source/app/app.cpp.s

source/module/CPPotify.o: source/module/CPPotify.cpp.o

.PHONY : source/module/CPPotify.o

# target to build an object file
source/module/CPPotify.cpp.o:
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11module.dir/build.make CMakeFiles/pybind11module.dir/source/module/CPPotify.cpp.o
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11app.dir/build.make CMakeFiles/pybind11app.dir/source/module/CPPotify.cpp.o
.PHONY : source/module/CPPotify.cpp.o

source/module/CPPotify.i: source/module/CPPotify.cpp.i

.PHONY : source/module/CPPotify.i

# target to preprocess a source file
source/module/CPPotify.cpp.i:
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11module.dir/build.make CMakeFiles/pybind11module.dir/source/module/CPPotify.cpp.i
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11app.dir/build.make CMakeFiles/pybind11app.dir/source/module/CPPotify.cpp.i
.PHONY : source/module/CPPotify.cpp.i

source/module/CPPotify.s: source/module/CPPotify.cpp.s

.PHONY : source/module/CPPotify.s

# target to generate assembly for a file
source/module/CPPotify.cpp.s:
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11module.dir/build.make CMakeFiles/pybind11module.dir/source/module/CPPotify.cpp.s
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11app.dir/build.make CMakeFiles/pybind11app.dir/source/module/CPPotify.cpp.s
.PHONY : source/module/CPPotify.cpp.s

source/module/authControl.o: source/module/authControl.cpp.o

.PHONY : source/module/authControl.o

# target to build an object file
source/module/authControl.cpp.o:
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11module.dir/build.make CMakeFiles/pybind11module.dir/source/module/authControl.cpp.o
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11app.dir/build.make CMakeFiles/pybind11app.dir/source/module/authControl.cpp.o
.PHONY : source/module/authControl.cpp.o

source/module/authControl.i: source/module/authControl.cpp.i

.PHONY : source/module/authControl.i

# target to preprocess a source file
source/module/authControl.cpp.i:
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11module.dir/build.make CMakeFiles/pybind11module.dir/source/module/authControl.cpp.i
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11app.dir/build.make CMakeFiles/pybind11app.dir/source/module/authControl.cpp.i
.PHONY : source/module/authControl.cpp.i

source/module/authControl.s: source/module/authControl.cpp.s

.PHONY : source/module/authControl.s

# target to generate assembly for a file
source/module/authControl.cpp.s:
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11module.dir/build.make CMakeFiles/pybind11module.dir/source/module/authControl.cpp.s
	$(MAKE) $(MAKESILENT) -f CMakeFiles/pybind11app.dir/build.make CMakeFiles/pybind11app.dir/source/module/authControl.cpp.s
.PHONY : source/module/authControl.cpp.s

# Help Target
help:
	@echo "The following are some of the valid targets for this Makefile:"
	@echo "... all (the default if no target is provided)"
	@echo "... clean"
	@echo "... depend"
	@echo "... edit_cache"
	@echo "... rebuild_cache"
	@echo "... pybind11app"
	@echo "... pybind11module"
	@echo "... source/app/app.o"
	@echo "... source/app/app.i"
	@echo "... source/app/app.s"
	@echo "... source/module/CPPotify.o"
	@echo "... source/module/CPPotify.i"
	@echo "... source/module/CPPotify.s"
	@echo "... source/module/authControl.o"
	@echo "... source/module/authControl.i"
	@echo "... source/module/authControl.s"
.PHONY : help



#=============================================================================
# Special targets to cleanup operation of make.

# Special rule to run CMake to check the build system integrity.
# No rule that depends on this can have commands that come from listfiles
# because they might be regenerated.
cmake_check_build_system:
	$(CMAKE_COMMAND) -S$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR) --check-build-system CMakeFiles/Makefile.cmake 0
.PHONY : cmake_check_build_system

