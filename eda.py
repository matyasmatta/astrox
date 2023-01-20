while True:
 heading = sense.get_compass()
 if heading < 45 or heading 315:
  sense.show_letter('N') 
