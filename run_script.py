import os, sys

def main():
  BASE_DIR = os.path.abspath(os.path.dirname(__file__))
  ROOT_DIR = BASE_DIR
  print("BASE_DIR", BASE_DIR)
  print("ROOT_DIR", ROOT_DIR)

  sys.path.insert(0, ROOT_DIR)
  sys.path.insert(0, os.path.join(ROOT_DIR, "packages"))

  os.environ.setdefault("FC_ROOT", ROOT_DIR)
  os.environ.setdefault("FC_CONF", "local")
  os.environ["DJANGO_SETTINGS_MODULE"] = "store_site.settings"

  import django
  django.setup()

  argv = list(sys.argv)
  argv.pop(0)

  import imp

  path = argv.pop(0)
  print(path)
  
  mod = imp.load_source("test", path)
  mod.main(argv)

if __name__ == "__main__":
  main()
