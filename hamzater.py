A                 = chr(0x0627);
b                 = chr(0x0628);
p                 = chr(0x0629);
t                 = chr(0x062A);
v                 = chr(0x062B);
j                 = chr(0x062C);
H                 = chr(0x062D);
x                 = chr(0x062E);
d                 = chr(0x062F);
dh                = chr(0x0630);
r                 = chr(0x0631);
z                 = chr(0x0632);
s                 = chr(0x0633);
sh                = chr(0x0634);
S                 = chr(0x0635);
D                 = chr(0x0636);
T                 = chr(0x0637);
Z                 = chr(0x0638);
E                 = chr(0x0639);
g                 = chr(0x063A);
f                 = chr(0x0641);
q                 = chr(0x0642);
k                 = chr(0x0643);
l                 = chr(0x0644);
m                 = chr(0x0645);
n                 = chr(0x0646);
h                 = chr(0x0647);
w                 = chr(0x0648);
Y                 = chr(0x0649);
y                 = chr(0x064A);
tatw              = chr(0x0640);
hamza             = chr(0x0621);
hamza_above       = chr(0x0654);
hamza_below       = chr(0x0655);
F                 = chr(0x064b);
N                 = chr(0x064c);
K                 = chr(0x064d);
a                 = chr(0x064e);
u                 = chr(0x064f);
i                 = chr(0x0650);
shaddah           = chr(0x0651);
o                 = chr(0x0652);
maddah_above      = chr(0x0653);
dagA              = chr(0x0670);
Awasl             = chr(0x0671);

harakaat_and_sukoon = { a, u, i, shaddah, o, F, N, K }
letters = {A, b, p, t, v, j, H, x, d, dh, r, z, s, sh, S, D, T, Z, E, g, f, q, k, l, m, n, h, w, Y, y , hamza }


class ConsonantInfo:
  cons = ""
  doubled = False
  vowel_mark = ""
  vowel = ""
  hamza = ""
  post_cons_str = ""
  def __str__(self):
    return "cons="+self.cons+", doubled="+str(self.doubled)+", vowel_mark="+self.vowel_mark+", vowel="+self.vowel

def build_cons_list(instr):
  cons_list = []
  index = 0
  while index < len(instr):
    assert instr[index] in letters
    cons_info = ConsonantInfo()
    cons_info.cons = instr[index]
    index += 1
    if index < len(instr) and instr[index] == o:
      cons_info.vowel_mark = o
      cons_info.vowel = o
      cons_info.post_cons_str += o
      index += 1
      cons_list.append(cons_info)
      continue
    if index < len(instr) and instr[index] == shaddah:
      cons_info.doubled = True
      cons_info.post_cons_str += shaddah
      index += 1
    if index < len(instr) and instr[index] == a:
      cons_info.vowel_mark = a
      cons_info.vowel = a
      cons_info.post_cons_str += a
      index += 1
      if index < len(instr) and instr[index] == A:
        cons_info.vowel += A
        cons_info.post_cons_str += A
        index += 1
      elif index < (len(instr)-1) and instr[index:(index+2)] == Y+dagA:
        cons_info.vowel += A
        cons_info.post_cons_str += Y+dagA
        index+=2
      elif index < (len(instr)-1) and instr[index:(index+2)] == y+o:
        cons_info.vowel += y+o
        cons_info.post_cons_str += y+o
        index += 2
      elif index < (len(instr)-1) and instr[index:(index+2)] == w+o:
        cons_info.vowel += w+o
        cons_info.post_cons_str += w+o
        index += 2
      cons_list.append(cons_info)
      continue
    if index < len(instr) and instr[index] == i:
      cons_info.vowel_mark = i
      cons_info.vowel = i
      cons_info.post_cons_str += i
      index += 1
      if (index == (len(instr)-1) and instr[index] == y) or (index < (len(instr)-1) and instr[index] == y and instr[index+1] in letters):
        cons_info.vowel += y
        cons_info.post_cons_str += y
        index += 1
      cons_list.append(cons_info)
      continue
    if index < len(instr) and instr[index] == u:
      cons_info.vowel_mark = u
      cons_info.vowel = u
      cons_info.post_cons_str += u
      index += 1
      if (index == (len(instr)-1) and instr[index] == w) or (index < (len(instr)-1) and instr[index] == w and instr[index+1] in letters):
        cons_info.vowel += w
        cons_info.post_cons_str += w
        index += 1
    cons_list.append(cons_info)
  return cons_list

def print_cons_list(cons_list):
  print("------------")
  for x in cons_list:
    print(x)

def build_str(cons_list):
  retval = ""
  for x in cons_list:
    add_post_str = True
    if x.hamza != "":
      retval += x.hamza
      if x.hamza == A+maddah_above:
        add_post_str = False
    else:
      retval += x.cons
    if add_post_str:
      retval += x.post_cons_str
  return retval

def hamzate(instr):
  cons_list = build_cons_list(instr)
  for index in range(0, len(cons_list)):
    x = cons_list[index]
    if x.cons == hamza:
      if index == 0:
        # beginning
        if x.vowel == a+A:
          x.hamza = A+maddah_above
        elif x.vowel_mark == i:
          x.hamza = A+hamza_below
        else:
          x.hamza = A+hamza_above
      elif index == (len(cons_list)-1):
        # end
        prev_cons = cons_list[index-1]
        if (not prev_cons.vowel in { a+A, i+y, u+w, a+y+o, a+w+o } and
          not prev_cons.vowel_mark == o and
          not (prev_cons.cons == w and prev_cons.doubled and prev_cons.vowel_mark == u)):
          if prev_cons.vowel_mark == i:
            x.hamza = y+hamza_above
          elif prev_cons.vowel_mark == u:
            x.hamza = w+hamza_above
          else:
            if x.vowel_mark == i:
              x.hamza = A+hamza_below
            else:
              x.hamza = A+hamza_above
      else:
        # middle
        prev_cons = cons_list[index-1]
        #next_cons = cons_list[index+1]
        if prev_cons.vowel in { a+A, u+w, i+y, a+y+o, a+w+o }:
          if prev_cons.vowel in { i+y, a+y+o }:
            pass
          elif prev_cons.vowel in { u+w, a+w+o }:
            if x.vowel_mark == i:
              x.hamza = y+hamza_above
            else:
              if x.vowel == a+A and x.post_cons_str[-1] == A:
                x.hamza = A+maddah_above
              else:
                pass
              #pass
          else:
            if x.vowel_mark == i:
              x.hamza = y+hamza_above
            elif x.vowel_mark == u:
              x.hamza = w+hamza_above
            else:
              pass
        elif prev_cons.vowel_mark == o:
          if x.vowel_mark == i:
            x.hamza = y+hamza_above
          elif x.vowel_mark == u:
            x.hamza = w+hamza_above
          else:
            if x.vowel == a+A and x.post_cons_str[-1] == A:
              if x.doubled:
                pass
              else:
                x.hamza = A+maddah_above
            else:
              x.hamza = A+hamza_above
        elif x.vowel_mark == o:
          if prev_cons.vowel_mark == i:
            x.hamza = y+hamza_above
          elif prev_cons.vowel_mark == u:
            x.hamza = w+hamza_above
          else:
            x.hamza = A+hamza_above
        else:
          if x.vowel_mark == i or prev_cons.vowel_mark == i:
            x.hamza = y+hamza_above
          elif x.vowel_mark == u or prev_cons.vowel_mark == u:
            x.hamza = w+hamza_above
          else:
            if x.vowel == a+A and x.post_cons_str[-1] == A:
              if x.doubled:
                pass
              else:
                x.hamza = A+maddah_above
            else:
              x.hamza = A+hamza_above

  apply_tatweel = True
  if apply_tatweel:
    for index in range(1, len(cons_list)-1):
      x = cons_list[index]
      prev_cons = cons_list[index-1]
      if (x.cons == hamza and x.hamza == "" and 
        A not in prev_cons.post_cons_str and
        d not in prev_cons.post_cons_str and
        dh not in prev_cons.post_cons_str and
        r not in prev_cons.post_cons_str and
        z not in prev_cons.post_cons_str and
        w not in prev_cons.post_cons_str):
        x.hamza = tatw+hamza_above

  outstr = build_str(cons_list)
  return outstr

do_test = False
if do_test:
  word_list = ["ءِسْلَام", "ءَامَنَ", "ءَسْلَمَ", "ءُرِيدُ", "ءِسْلَام", "ءِيمَان", "ءُوخِذَ", "دُعَاءُ", "سُوءُ", "جِيءَ", "ضَوْءَ", "شَيْءَ", "بُطْءُ", "عِبْءُ", "شَطْءُ", "تَبَوُّءُ", "يُهَدِّء", "سَيِّء", "بَطُء", "يَهْدَء", "مُبْتَدَء", "هَيْءَة", "خَطِيءَة", "بَرِيءُونَ", "بَرِيءَانِ", "بَرِيءِينَ", "بَرِيءَيْنِ", "شَيْءُهُ", "شَيْءَهُ", "شَيْءِهِ", "شَيْءَانِ", "شَيْءَيْنِ", "مَجِيءُهُ", "مَجِيءَهُ", "مَجِيءِهِ", "سُوءِهِ", "ضَوْءِهِ", "سُوءَهُ", "سُوءَانِ", "تَوْءَم", "ضَوْءَهُ", "ضَوْءَانِ", "سُوءُهُ", "يَسُوءُونَ", "سَاءِل", "تَسَاءُل", "تَسَاءَلَ", "قِرَاءَات", "جُزْءَانِ", "عِبْءَانِ", "عِبْءَيْنِ", "بُطْءَهُ", "بُطْءُهُ", "بُطْءِهِ", "مَسْءُول", "تَرْءِيس", "مِرْءَاة", "ظَمْءَان", "مَسْءَلَة", "الْمَرْءَة", "بِءْسَ", "سُءْلَكَ", "كَءْس", "سُءِلَ", "يَءِسَ", "مُتَّكِءِينَ", "رَءِيس", "سُءَال", "رُءُوس", "لُءَيّ", "شَنَءَان", "سَءَلَ", "رَءَىٰ", "رَءَسَ", "يُرَءِسُ", "رُءِّسَ", "تَفَءُّل", "يُبَرِّءُونَ", "يُبَرَّءُونَ", "سَءَّال", "لَءَّال"]

  for x in word_list:
    print(hamzate(x))

import sys
print(hamzate(sys.argv[1]))

