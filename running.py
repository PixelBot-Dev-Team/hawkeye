import sys, os, time, threading, subprocess, fnmatch, pathlib

CurrentDir = pathlib.Path(__file__).parent.absolute()

class SourceChangeMonitor(threading.Thread):
                                                                                      
        _process = None
                                                           
        POLL_INTERVAL = 3

        FILE_PATTERN = r"[!.]*.py"
                                                 
        ROOT_DIRECTORY = CurrentDir
                                                                                       
        PROGRAM = r"main.py"

        #initialize timed restart
        lastRestart = time.time()
        nextRestart = time.time() + 3600

        def __init__(self):
                threading.Thread.__init__(self)
                self.this_script_name = os.path.abspath( sys.argv[0] )
                self.files = self.get_files()
                self.start_program()

        def run(self):
                while 1:
                        time.sleep(self.POLL_INTERVAL)
                        if self.poll():
                                print( "-------------------------------------------------")
                                print( "Noticed a change in program source. Restarting...")
                                print( "-------------------------------------------------")
                                self.start_program()
                                self.lastRestart = time.time()
                                self.nextRestart = time.time() + 3600
                        else:
                                #check if program crashed
                                if self._process.poll() is not None:
                                        print( "-------------------------------------------------")
                                        print( "Program crashed. Restarting...")
                                        print( "-------------------------------------------------")
                                        self.start_program()
                                        self.lastRestart = time.time()
                                        self.nextRestart = time.time() + 3600
                                else:
                                    print("Next restart in:", int((self.nextRestart - time.time()) / 60) , "minutes and", int((self.nextRestart - time.time()) % 60), "seconds")
                                    if time.time() > self.nextRestart:
                                            print( "-------------------------------------------------")
                                            print( "Restarting...")
                                            print( "-------------------------------------------------")
                                            self.start_program()
                                            self.lastRestart = time.time()
                                            self.nextRestart = time.time() + 3600

        def get_files(self):
                """                                                                                                          
                Get a list of all files along with their timestamps for last modified                                        
                """
                files = []
                for root, dirnames, filenames in os.walk(self.ROOT_DIRECTORY):
                        for filename in fnmatch.filter(filenames, self.FILE_PATTERN):
                                full_filename = os.path.join(root, filename)
                                files.append(full_filename)

                # Attach the last modified dates                                                                             
                files = [(f, os.stat(f).st_mtime) for f in  files]

                # Don't include this script                                                                                  
                files = [f for f in files if  f[0] != self.this_script_name]
                return list(files)

        def poll(self):
                """                                                                                                                          Check if any source files have changed since last poll. Returns True if                                                      files have changed, False otherwise                                                                                          """
                new_files = self.get_files()
                if self.files != new_files:
                        self.files = new_files
                        return True
                return False

        def start_program(self):
                """                                                                                                                          Start the program. If it was already started, kill it before restarting                                                      """
                if self._process != None and self._process.poll() is None:
                        self._process.kill()
                        self._process.wait()

                self._process = subprocess.Popen( [sys.executable, self.PROGRAM] )



if __name__ == "__main__":
        SourceChangeMonitor().start()
