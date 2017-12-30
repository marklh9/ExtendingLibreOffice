
if __name__ == "__main__":
    import subprocess
    import platform
    import uno
    from dummytextjob import DummyTextJob


    if platform.system() == "Windows":
        binary = "soffice.exe"
    else:
        binary = "soffice"

    process = subprocess.Popen([binary, "--accept=socket,host=localhost,port=2002;urp;'", "--writer"], shell=True )

    local_context = uno.getComponentContext()
    resolver = local_context.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_context)

    ctx = None

    while ctx is None:
        try:
            ctx = resolver.resolve(
                "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        except: pass

    job = DummyTextJob(ctx)
    job.trigger(())
