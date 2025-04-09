import re
import tkinter as tk
import inflect
import spacy
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Trie():

    def __init__(self):
        self._end = '*'
        self.trie = dict()

    def __repr__(self):
        return repr(self.trie)

    def add_word(self, word):
        temp_trie = self.trie
        for letter in word:
            if letter in temp_trie:
                temp_trie = temp_trie[letter]
            else:
                temp_trie = temp_trie.setdefault(letter, {})
        temp_trie[self._end] = self._end
        return temp_trie

    def find_word(self, word):
        sub_trie = self.trie
        for letter in word:
            if letter in sub_trie:
                sub_trie = sub_trie[letter]
            else:
                return False
        if self._end in sub_trie:
            return True
        else:
            return False


class Spell_Grammar_Checker(customtkinter.CTk):

    #interface
    def __init__(self):
        super().__init__()
        self.load()
        # configure window
        self.title("Dissertation")
        self.geometry(f"{1000}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Rule-based\nNatural Language\nProcessor", 
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))


        self.home_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Grammar Checker",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Limitations",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
        self.review_label = customtkinter.CTkLabel(self.sidebar_frame, text="Give Feedback:", anchor="w")
        self.review_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.review_button = customtkinter.CTkButton(self.sidebar_frame, text="Click Here",
                                                           command=self.open_input_dialog_event)
        self.review_button.grid(row=10, column=0, padx=20, pady=(10, 30))


        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        #self.home_frame.grid_columnconfigure(0, weight=1)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        #create about frame within home frame
        self.about = customtkinter.CTkFrame(self.home_frame)
        self.about.grid(padx=(20, 20), pady=(20, 0)) 
        self.about_label = customtkinter.CTkLabel(master=self.about, width=600, text="About:", font=customtkinter.CTkFont(size=28, weight="bold"), anchor="w")
        self.about_label.grid(row=0, column=0, padx=30, pady=30)   
        self.writeup = customtkinter.CTkLabel(master=self.about, text="\tEnglish is the most popular language in the world. There are about 400 million people using English as first language, but more than one billion people use it as a second language. With the increasing update of computers and the Internet, tens of thousands of users tend to write and communicate in English in their daily work. Users, whose native language is not English, easily make two different kinds of mistakes while writing: spelling and grammar mistakes. Hence, it is difficult to adapt to every rule and constraint of the language and apply seamlessly in communication which makes an English language error detection software so crucial in everyday lives.\n\n\tIn this project, we have developed a Spell checker using a Trie and suggested corrections based on the edit (Levenshtein) distance between the incorrectly spelled word and the correct word. In addition to this, we have also implemented Grammar checking, on a correctly spelled sentence which is taken as input, using a rule-based approach. The proposed application deals with dynamic text input given on a Graphical User Interface which is then passed for spell checking as well as grammar checking.", justify="left", font=customtkinter.CTkFont(size=18), wraplength=600)
        self.writeup.grid(row=1, column=0, padx=30, pady=(0,30)) 


        #create grammar check frame within second frame
        self.check_frame = customtkinter.CTkFrame(self.second_frame)
        self.check_frame.grid(padx=(20, 20), pady=(20, 0))    
        self.check_group = customtkinter.CTkLabel(master=self.check_frame, width=500, text="Grammar Checker", 
                                                  font=customtkinter.CTkFont(size=28, weight="bold"), anchor="w")
        self.check_group.grid(row=0, column=0, padx=(30,0), pady=(10,0))    

        # create text
        self.text = customtkinter.CTkTextbox(self.check_frame, height=300, width=400, wrap="word", 
                                             font=customtkinter.CTkFont(size=20))
        self.text.grid(row=1, column=0, padx=(30, 20), pady=(20, 0), sticky="nsew")


        #instruction
        self.instruction_frame = customtkinter.CTkFrame(self.check_frame)
        self.instruction_frame.grid(row=1, column=1, padx=(0, 30), pady=(20, 0), sticky="nsew")
        self.label_group = customtkinter.CTkLabel(master=self.instruction_frame, text="Let's get started:\n\nStep 1: Add your text, click the submit button and the errors will be highlighted.\n\nStep 2: Double click the highlighted words/phrases to see suggestions.\n\nStep 3: Click on a suggestion to accept it.\n\nStep 4: Use the delete button to clear the screen.", justify="left", wraplength=180)
        self.label_group.grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky="ew")


        # create submit button
        self.submit_button = customtkinter.CTkButton(self.check_frame, text="Submit", command=self.task)
        self.submit_button.grid(row=5, column=0, padx=20, pady=10)

        # create delete button
        self.listbox=None
        self.delete_button = customtkinter.CTkButton(self.check_frame, width=100, text="Delete", command=self.delete)
        self.delete_button.grid(row=5, column=1, padx=(0,30), pady=10)

        #create limitation frame within third frame
        self.about = customtkinter.CTkFrame(self.third_frame)
        self.about.grid(padx=(20, 20), pady=(20, 0)) 
        self.about_label = customtkinter.CTkLabel(master=self.about, width=600, text="Limitations:", font=customtkinter.CTkFont(size=28, weight="bold"), anchor="w")
        self.about_label.grid(row=0, column=0, padx=30, pady=30)   
        self.writeup = customtkinter.CTkLabel(master=self.about, text="1. Since we have used a rule-based approach, our grammar checker cannot predict missing words.\n\n2. Handles a limited set of verb tenses, such as present, past, continuous, and perfect.\n\n3. Sentences are relatively simple and do not have complex structures, such as embedded clauses, passive voice, or modal verbs.\n\n4. Does not handle cases where words have multiple meanings or where sentence structures are ambiguous.\n\n5. Checks errors in subject-verb agreement and does not detect other grammar errors, such as sentence fragments or run-on sentences.\n\n6. Cannot handle collective nouns, indefinite pronouns, or irregular verbs for subject verb agreement.",justify="left", font=customtkinter.CTkFont(size=18), wraplength=600)
        self.writeup.grid(row=1, column=0, padx=30, pady=(0,30)) 

        # set default values
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        self.text.insert("1.0", "Start writing here")

        # select default frame
        self.select_frame_by_name("home")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Write a review:", title="User Review")
        print("Review:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def delete(self):
        if self.listbox is not None:
            self.listbox.destroy()
        self.text.delete("1.0", tk.END)
        global sva
        if sva!=None:
            sva.clear()
        print(sva)
        global sentences
        if sentences!=None:
            sentences.clear()

    def replace_word(self,event,error_index,start,end):
        widget = event.widget
        selection = widget.curselection()
        print(selection)
        if selection:
            index = selection[0]
            new_word=self.listbox.get(index)
        
        # Replace the error word with the selected word
        self.text.delete(start,end)
        self.text.insert(start, new_word, tags=None)
        # Destroy the listbox
        self.listbox.destroy()



    #loading dictionary
    def load(self):
        with open('words_frequency.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split('\t')
                    if len(parts) == 2:
                        word, freq = parts
                        word_freq_dict[word] = int(freq)
            for word,freq in word_freq_dict.items():
                my_trie.add_word(word)

    #extracting text from input box
    def get_text(self):
        text = self.text.get("1.0", tk.END)
        return text
    

    #spell check
    def _level_one_edits(self,word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)] #Generates all possible splits of the error word
        deletes = [l + r[1:] for l,r in splits if r]
        swaps = [l + r[1] + r[0] + r[2:] for l, r in splits if len(r)>1]
        replaces = [l + c + r[1:] for l, r in splits if r for c in letters]           
        inserts = [l + c + r for l, r in splits for c in letters if c]
        return set(deletes + swaps + replaces + inserts)

    def _level_two_edits(self,word): 
        level_one_edits = self._level_one_edits(word)
        level_two_edits = set()
        for edit in level_one_edits:
            level_two_edits.update(self._level_one_edits(edit))
        return level_two_edits
    
    def generate_spelling_suggestions(self,word):
        level_one_edits = self._level_one_edits(word)
        level_one_edits = [w for w in level_one_edits if my_trie.find_word(w)==True and w[0].lower()==word[0].lower()]
        level_two_edits = self._level_two_edits(word)
        level_two_edits = [w for w in level_two_edits if my_trie.find_word(w)==True and w[0].lower()==word[0].lower()]

        candidates_1 = sorted([(c,word_freq_dict[c]) for c in level_one_edits], key=lambda tup: tup[1], reverse=True)
        candidates_2 = sorted([(c,word_freq_dict[c]) for c in level_two_edits], key=lambda tup: tup[1], reverse=True)
        result = candidates_1
        result.extend(y for y in candidates_2 if y not in candidates_1)
        spelling_suggestions.clear()

        for i,j in result:
            spelling_suggestions.append(i)

        return spelling_suggestions
    
    def on_double_click_spelling_suggestions(self,event,word, start, end):
        error_index = self.text.index(tk.CURRENT)
        # Get the word itself
        word = self.text.get(error_index+" wordstart",error_index+" wordend")
        # Remove the previous listbox, if it exists
        if self.listbox is not None:
            self.listbox.destroy()
        # Generate suggestions for the clicked word
        suggestions = self.generate_spelling_suggestions(word)
        # Create a listbox with the suggestions
        self.listbox = tk.Listbox(self.text, height=min(len(suggestions), 10), font=customtkinter.CTkFont(size=20))
        for suggestion in suggestions:
            self.listbox.insert(tk.END, suggestion)
        
        # Get the coordinates of the clicked word
        x, y, width, height = self.text.bbox(error_index)
        # Calculate the coordinates to display the listbox
        self.listbox.place(x=x+15, y=36+y)
        self.listbox.bind("<<ListboxSelect>>", lambda event: self.replace_word(event,error_index,start, end))

    def spell_check(self,content):
        doc=nlp(content)
        for word in doc:
            if(word.ent_type_=='PERSON' or word.ent_type_=='DATE' or word.ent_type_=='TIME' or word.ent_type_=='MONEY' or word.ent_type_=='PERCENT' or word.ent_type_=='QUANTITY' or word.ent_type_=='ORDINAL' or word.ent_type_=='CARDINAL'):
                continue
            elif (word.pos_=='PRON') or (my_trie.find_word(word.text.lower())==True):
                continue
            elif (word.text =='\'s') or (word.text == 's\''):
                continue
            elif (word.text in punctuations):
                continue
            elif (word.text.lower() in contractions):
                continue
            elif(word.text.isupper()):
                continue
            elif (len(word.text)==1 and word.text.isalpha()):
                continue
            elif (word.text=='\n' or word.text==' '):
                continue
            else:
                # Compile regular expression pattern to match the error word
                pattern = re.compile(r'\b' + word.text + r'\b')
                # Find error word using regular expression pattern
                for match in re.finditer(pattern,content):
                    position = match.start()
                start = f"1.{position}"
                end = f"1.{position + len(word.text)}"
                self.text.tag_config("SE",foreground="red",underline=False)
                self.text.tag_add("SE",start,end)
            
                self.text.tag_bind("SE","<Double-Button-1>", lambda event: self.on_double_click_spelling_suggestions(event,word.text.lower(),start,end))
                self.listbox=None


    #grammar check
    def on_double_click_grammar_suggestions(self,event,suggestion, start, end):
        gram_error_index = self.text.index(tk.CURRENT)
        if self.listbox is not None:
            self.listbox.destroy()
        # Create a listbox with the suggestions
        self.listbox = tk.Listbox(self.text, height=1, font=customtkinter.CTkFont(size=20))
        self.listbox.insert(tk.END, suggestion)
        # Get the coordinates of the clicked word
        x, y, width, height = self.text.bbox(gram_error_index)
        # Calculate the coordinates to display the listbox
        self.listbox.place(x=x+15, y=36+y)
        self.listbox.bind("<<ListboxSelect>>", lambda event: self.replace_word(event,gram_error_index,start, end))

    def uppercase_first_letter(self,word):
        ascii_val = ord(word[0])
        if 97 <= ascii_val <= 122:  # Check if the first letter is lowercase
            uppercase_ascii_val = ascii_val - 32  # Add ASCII value difference to convert to uppercase
            uppercase_letter = chr(uppercase_ascii_val)  # Convert back to character
            return uppercase_letter + word[1:]  # Combine the converted letter with the rest of the word
        else:
            return word  # If the first letter is already uppercase or not a letter, return the original word
    
    def first_letter_capitalized(self,text):
        # Parse the text with Spacy
        doc1 = nlp(text)
        print(text)
        # Iterate over each sentence in the parsed document
        for sentence in doc1.sents:
            print(sentence)
            first_word=sentence[0].text
            if (ord(first_word[0]) >= 65 and ord(first_word[0]) <= 90):
                continue
            else:
                error_ch=first_word
                print(first_word[0])
                # Capitalize the first letter of the sentence
                correct_word=self.uppercase_first_letter(error_ch)
                fl_cap[error_ch]=correct_word
        return fl_cap

    def article_agreement(self,content):  
    # Parse the sentence with Spacy
        doc1 = nlp(content)
        # Iterate through each token in the sentence
        for i, token in enumerate(doc1):
            if token.pos_=="PUNCT":
                prev_word=doc1[i-1]
                if(prev_word.text in ["a","an","the"]):
                    error=doc1[i-1].text + doc1[i].text
                    error_suggestion_article[error]=token.text
            elif(token.text in ["a.","an.","the."]):
                error_suggestion_article[token.text]="."
            # Check if the token is an article (i.e., "a", "an", or "the")
            elif token.pos_ == "DET" and token.text.lower() in ["a", "an", "the"]:
                article = token.text
              
                next_word=doc1[i+1]
                #Check if the next word is a country or city or mountain or person name
                if(next_word.ent_type_ in ["GPE","LOC","PERSON"]) or (next_word.pos_ not in ["NOUN","ADJ"]):
                    print(next_word.ent_type_)
                    error_suggestion_article[article]=next_word
                elif (next_word.pos_=="NOUN"):
                    if(next_word.tag_=="NN" or next_word.tag_=="NNP"):
                        ca=p.an(next_word.text)

                        if (article.lower()=="the"):
                            continue
                        elif(article.lower()!=ca.split()[0]):
                            error_article=article+" "+next_word.text
                            error_suggestion_article[error_article]=ca

                    elif(next_word.tag_=="NNS" or next_word.tag_=="NNPS"):
                        if(article.lower()!="the"):
                            error_article=article+" "+next_word.text
                            ca="the"+" "+next_word.text
                            error_suggestion_article[error_article]=ca
                elif next_word.pos_=="ADJ":
                    ca=p.an(next_word.text)
                    if (article.lower()=="the"):
                        continue
                    elif(article.lower()!=ca.split()[0]):
                        error_article=article+" "+next_word.text
                        error_suggestion_article[error_article]=ca
        return error_suggestion_article
   
    def singular(self,word):
        if(p.singular_noun(word)==False):
            return 1
        else:
            return 0
        
   
    def split_compound_sentence(self,sentence):
        conjunctions=["and","or","but","yet","so","thus","therefore"]
        clauses = []
        current_clause = []
        for token in sentence:
                if token.text.lower() in conjunctions:
                # Found a coordinating conjunction, so store current clause and start a new one
                    clauses.append(' '.join(current_clause))
                    current_clause = []
                else:
                    # Add current token to current clause
                    current_clause.append(token.text)
        # Append the last clause
        clauses.append(' '.join(current_clause))
        # Return list of clauses
        return clauses

    def check_sva(self,subject,main_verb,auxiliary_verb,auxiliary_verb_2):
        print(subject,main_verb,auxiliary_verb,auxiliary_verb_2)
        if subject and main_verb and auxiliary_verb:
            if(main_verb.tag_ == "VBG" and auxiliary_verb and auxiliary_verb_2):
                sva=self.perfect_continous(subject,main_verb,auxiliary_verb,auxiliary_verb_2)
            elif(main_verb.tag_ == "VBG"):
                sva=self.continous(subject,main_verb,auxiliary_verb)
            elif(main_verb.tag_ == "VBN"):
                sva= self.perfect(subject,main_verb,auxiliary_verb)
        else:
            sva=self.simple(subject,main_verb,auxiliary_verb)
        return sva

    def simple(self,subject,main_verb,auxiliary_verb):
        if auxiliary_verb:
            verb = auxiliary_verb.text 
        elif main_verb == None or main_verb.tag_ == "VBD":
            return
        elif main_verb:
            verb = main_verb.text 
        else:
            return

        if subject==None:
            return
        if subject.text== "I":
            if verb in ["were","is","are","has"]:
                error_verb=verb
                if(verb in ["is","are"]):
                    suggestion_verb="am"
                elif(verb in ["were"]):
                    suggestion_verb="was"
                elif(verb in ["has"]):
                    suggestion_verb="have"
                sva[error_verb]=suggestion_verb
            elif(self.singular(verb)!=1) and verb not in ["have","am","was"]:
                error_verb =verb
                if main_verb.lemma_ != main_verb.text:
                    suggestion_verb = main_verb.lemma_
                sva[error_verb]=suggestion_verb
        else:
            if ((self.singular(subject.text)==0) and (self.singular(verb)!=1) and verb not in("have","had","are","were")): 
                error_verb=verb
                if verb == "has":
                    suggestion_verb = "have"
                elif verb == "is":
                    suggestion_verb = "are"
                elif verb == "was":
                    suggestion_verb = "were"
                else:
                    if main_verb.lemma_ != main_verb.text:
                        suggestion_verb = main_verb.lemma_
                sva[error_verb]=suggestion_verb
            
            elif((self.singular(subject.text)==1) and (self.singular(verb)!=0) and verb not in("has","had","is","was")):
                error_verb=verb
                if verb == "have":
                    suggestion_verb = "has"
                elif verb == "are":
                    suggestion_verb = "is"
                elif verb == "were":
                    suggestion_verb = "was"
                else:
                    verb = main_verb.lemma_
                    suggestion_verb = p.plural_noun(verb)
                sva[error_verb]=suggestion_verb
        return sva
    
    def perfect_continous(self,subject,main_verb,auxiliary_verb,auxiliary_verb_2):
        if(main_verb.tag_ == "VBG" and auxiliary_verb and auxiliary_verb_2):
            if auxiliary_verb and main_verb.tag_ == "VBG":
                if ((subject.tag_ == "PRP" and subject.lower_ =="i" and auxiliary_verb.lower_ not in ["have","had"])):
                    error_verb=auxiliary_verb.text+" "+auxiliary_verb_2.text+" "+main_verb.text
                    suggestion_verb="have been "+main_verb.text
                    sva[error_verb]=suggestion_verb
                elif ((subject.tag_ == "NNS" or subject.tag_ == "PRP") and (self.singular(subject.text) == 0)) and (auxiliary_verb.lower_ not in ["have","had"] ):
                    error_verb=auxiliary_verb.text+" "+auxiliary_verb_2.text+" "+main_verb.text
                    suggestion_verb="have been "+main_verb.text
                    sva[error_verb]=suggestion_verb
                elif ((subject.tag_ == "NN" or subject.tag_ == "NNP" or subject.tag_ == "PRP") and (subject.text not in ["They","We","I"])) and (auxiliary_verb.lower_ not in ["has","had"]):
                    error_verb=auxiliary_verb.text+" "+auxiliary_verb_2.text+" "+main_verb.text
                    suggestion_verb="has been "+main_verb.text
                    sva[error_verb]=suggestion_verb
        return sva 
        
    def perfect(self,subject,main_verb,auxiliary_verb):
        if auxiliary_verb and main_verb.tag_ == "VBN":
            if ((subject.tag_ == "PRP" and subject.lower_ =="i" and (auxiliary_verb.lower_  not in ["have","had"]))):
                error_verb=auxiliary_verb.text+" "+main_verb.text
                suggestion_verb="have "+main_verb.text
                sva[error_verb]=suggestion_verb
            elif ((subject.tag_ == "NNS" or subject.tag_ == "PRP") and (self.singular(subject.text) == 0)) and (auxiliary_verb.lower_ not in ["have","had"]):
                error_verb=auxiliary_verb.text+" "+main_verb.text
                suggestion_verb="have "+main_verb.text
                sva[error_verb]=suggestion_verb
            elif ((subject.tag_ == "NN" or subject.tag_ == "NNP" or subject.tag_ == "PRP") and (subject.text not in ["They","We","I"])) and (auxiliary_verb.lower_ not in ["has","had"]):
                error_verb=auxiliary_verb.text+" "+main_verb.text
                suggestion_verb="has "+main_verb.text
                sva[error_verb]=suggestion_verb
        return sva

    def continous(self,subject,main_verb,auxiliary_verb):
        if auxiliary_verb and main_verb.tag_ == "VBG":
            if ((subject.tag_ == "PRP" and subject.lower_ =="i" and auxiliary_verb.lower_ not in ["am","was"])):
                error_verb=auxiliary_verb.text+" "+main_verb.text
                if(auxiliary_verb.lower_ in ["is","are"]):
                    suggestion_verb="am "+main_verb.text
                elif(auxiliary_verb.lower_ =="were"):
                    suggestion_verb="was "+main_verb.text
                else:
                    suggestion_verb="am "+main_verb.text
                sva[error_verb]=suggestion_verb
            elif ((subject.tag_ == "NNS" or subject.tag_ == "PRP") and (self.singular(subject.text) == 0)) and (auxiliary_verb.lower_ not in ["are", "were"] ):
                error_verb=auxiliary_verb.text+" "+main_verb.text
                if(auxiliary_verb.lower_ in ["am","is"]):
                    suggestion_verb="are "+main_verb.text
                elif(auxiliary_verb.lower_=="was" ):
                    suggestion_verb="were "+main_verb.text
                else:
                    suggestion_verb="are "+main_verb.text
                sva[error_verb]=suggestion_verb
            elif ((subject.tag_ == "NN" or subject.tag_ == "NNP" or subject.tag_ == "PRP") and (subject.text not in ["They","We","I"])) and (auxiliary_verb.lower_ not in ["is","was"]):
                error_verb=auxiliary_verb.text+" "+main_verb.text
                if(auxiliary_verb.lower_ in ["am","are"]):
                    suggestion_verb="is "+main_verb.text 
                elif(auxiliary_verb.lower_ =="were"):
                    suggestion_verb="was "+main_verb.text 
                else:
                    suggestion_verb="is "+main_verb.text
                sva[error_verb]=suggestion_verb
        return sva
    
    def sub_verb(self,sentence):
        doc = nlp(sentence)
        # Get the subject, main verb and auxiliary verb tokens for the sentence
        subject = None
        main_verb = None
        auxiliary_verb = None
        auxiliary_verb_2 = None
        for token in doc:
            if token.dep_ == "nsubj":
                subject = token
                print("Noun or Pronoun: ",subject)
            elif token.pos_ == "VERB" or token.pos_ == "ADP":
                if token.tag_ == "IN":
                    continue
                if not main_verb:
                    main_verb = token
                    print("main verb: ",main_verb)
            elif token.dep_== "aux" or token.pos_ == "AUX":
                if token.tag_ == "TO":
                    continue
                if auxiliary_verb:
                    auxiliary_verb_2 = token
                    print("auxiliary verb 2: ",auxiliary_verb_2)
                else:
                    auxiliary_verb = token
                    print("auxiliary verb: ",auxiliary_verb)
            
        sva=self.check_sva(subject,main_verb,auxiliary_verb,auxiliary_verb_2)
        return sva
    
    def subject_verb_agreement(self,content):
        doc = nlp(content)
        subjects = []
        verbs = []
        
        for token in doc:
            if token.pos_ == "VERB" or token.pos_ == "AUX":
                verbs.append(token)
            elif token.dep_ == "nsubj" or token.dep_ == "nsubjpass":
                subjects.append(token)

        for sent in doc.sents:
            sentences.append(sent)
        for sentence in sentences:
            if len(subjects) >= 1 and len(verbs) > 1:
                clauses=self.split_compound_sentence(sentence)

                # Get the subject, main verb and auxiliary verb tokens for the sentence
                for clause in clauses:
                    sva=self.sub_verb(clause)
            else:
                sva=self.sub_verb(str(sentence))
        return sva
    
    def grammar_check(self,content):
        gram_error_suggestion={}
        fl_cap = {}
        gram_error_suggestion.clear()
        fl_cap.clear()
        error_suggestion_article=self.article_agreement(content)
        fl_cap=self.first_letter_capitalized(content)
        print(fl_cap)
        gram_error_suggestion.update(fl_cap)
        gram_error_suggestion.update(error_suggestion_article)
        sva=self.subject_verb_agreement(content)
        if gram_error_suggestion!=None:
            for e, suggestion in gram_error_suggestion.items():
                pattern_a = re.compile(r'\b' + e + r'\b')
                for match in re.finditer(pattern_a, content):
                    start = match.start()
                    end = match.end()
                    print(start)
                    print(end)
                    wdstart = f"1.{start}"
                    wdend = f"1.{end}"
                    self.text.tag_add(e,wdstart,wdend )
                    self.text.tag_config(e, foreground="blue", underline=True)
                    self.text.tag_bind(e,"<Double-Button-1>", lambda event, s=suggestion: self.on_double_click_grammar_suggestions(event, s, wdstart, wdend))
                    self.listbox=None
            
        if sva!=None:
            for e, suggestion in sva.items():
                pattern_a = re.compile(r'\b' + e + r'\b')
                for match in re.finditer(pattern_a, content):
                    start = match.start()          
                    end = match.end()
                    wdstart = f"1.{start}"
                    wdend = f"1.{end}"
                    self.text.tag_add(e, wdstart, wdend)
                    self.text.tag_config(e, foreground="blue", underline=True)
                    self.text.tag_bind(e,"<Double-Button-1>", lambda event, s=suggestion: self.on_double_click_grammar_suggestions(event, s, wdstart, wdend))
                    self.listbox=None


    #calling grammar and spell check functions
    def task(self):
        content=self.get_text()
        self.grammar_check(content)
        self.spell_check(content)
                      
                
my_trie=Trie()
word_freq_dict={}
spelling_suggestions=[]
error_suggestion_article={}
fl_cap={}
punctuations='''!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~'''
#For contractions
contractions={"n\'t" : "not","\'re" : " are","\'s" : "is","\'d" : " would", "\'ll" : " will","\'ve" : " have","\'m":"am"}

nlp = spacy.load('en_core_web_sm')
sentences=[]
sva={}
p = inflect.engine()

app = Spell_Grammar_Checker()
app.mainloop()