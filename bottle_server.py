from bottle import route, run, template, static_file, redirect
import os
import os.path

filtered_images = []
total_filtered_images = 0
total_cirrus_images = 0
total_cumulus_images = 0
total_mixed_images = 0

@route('/')
def root():
  get_image_between_ten_to_one()
  total_filtered_images = len(filtered_images)
  total_cirrus_images = file_count('./data_images/classified/cirrus/')
  total_cumulus_images = file_count('./data_images/classified/cumulus/')
  total_mixed_images = file_count('./data_images/classified/mixed/')
  return template("""
  <h1> Report</h1>
  <p>Total_filtered_images = {{total_filtered_images}}</p>
  <p>Total_cirrus_images = {{total_cirrus_images}}</p>
  <p>Total_cumulus_images = {{total_cumulus_images}}</p>
  <p>Total_mixed_images = {{total_cumulus_images}}</p>
  <a href="/image_question/0">Start Classifying</a>
  """, total_filtered_images = total_filtered_images, total_cirrus_images = total_cirrus_images, total_cumulus_images = total_cumulus_images)


@route('/image_question/<index>')
def index(index):
  total_cirrus_images = file_count('./data_images/classified/cirrus/')
  total_cumulus_images = file_count('./data_images/classified/cumulus/')
  total_mixed_images = file_count('./data_images/classified/mixed/')
  return template("""
  <a href="/add_as_cirrus/{{index}}">Cirrus</a>
  &nbsp;
  <a href="/add_as_cumulus/{{index}}">Cumulus</a>
  &nbsp;
  <a href="/add_as_mixed/{{index}}">Mixed</a>
  &nbsp;
  <a href="/image_question/{{int(index) +10}}">+10</a>
  &nbsp;
  <a href="/image_question/{{int(index) +30}}">+30</a>
  &nbsp;


  {{file_name}}
  <p>Total_filtered_images = {{total_filtered_images}} Total_cirrus_images = {{total_cirrus_images}} Total_cumulus_images = {{total_cumulus_images}} Total_mixed_images = {{total_mixed_images}}</p>
  <img src="/pictures/{{index}}"/>
  """, index=index, file_name=filtered_images[int(index)], total_filtered_images=total_filtered_images,
  total_cirrus_images= total_cirrus_images, total_cumulus_images=total_cumulus_images, total_mixed_images=total_mixed_images)


@route('/pictures/<index>')
def serve_pictures(index):
  image_file_name = filtered_images[int(index)]
  print(image_file_name)
  return static_file(image_file_name, root='./data_images/2017/' + image_file_name[:8])

@route('/add_as_cirrus/<index>')
def add_as_cirrus(index):
  move(index, 'cirrus')
  total_cirrus_images = file_count('./data_images/classified/cirrus/')
  redirect("/image_question/" + str(int(index)+30))

@route('/add_as_cumulus/<index>')
def add_as_cumulus(index):
  move(index, 'cumulus')
  total_cumulus_images = file_count('./data_images/classified/cumulus/')
  redirect("/image_question/" + str(int(index)+30))

@route('/add_as_mixed/<index>')
def add_as_mixed(index):
  move(index, 'mixed')
  total_mixed_images = file_count('./data_images/classified/mixed/')
  redirect("/image_question/" + str(int(index)+1))

def move(index, type):
  # add_as_mixed
  image_file_name = filtered_images[int(index)]
  os.system("cp ./data_images/2017/"+  image_file_name[:8] + '/' + image_file_name +" ./data_images/classified/"+ type +"/" + image_file_name)

  redirect("/image_question/" + str(int(index)+1))

def get_image_list():
  return get_image_between_ten_to_one()


def get_image_between_ten_to_one():
  for dirpath, dirnames, filenames in os.walk("./data_images/2017"):
    for filename in [f for f in filenames if f.endswith(".jpg") and time_from_file_name(f) >= 100000 and time_from_file_name(f) <= 130000]:
          filtered_images.append(filename)

  filtered_images.sort()

def file_count(path):
  path, dirs, files = next(os.walk(path))
  return len(files)


def time_from_file_name(filename):
  time = filename.split('.')[0][-6:]
  if len(time) == 0:
    # case for hidden file
    return 0
  return(int(time))


get_image_between_ten_to_one()
print(len(filtered_images)) #48769


run(host='localhost', port=8080, reloader=True)