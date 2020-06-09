# News Letter

We are only given the source file `newsletter.c`. At first glance it seems like
the program is well written, with the appropriate `malloc` and `free` statements.

I copied this to `newsletter-edit.c` and made some changes:
- Remove the alarm
- Resize the length of articles, edits, etc, so that we can test for buffer
  overflows more easily
- Add a `print_state` function and run it every menu invocation:
```c
void print_state() {
    puts("===========================");
    for (int i = 0; i < ARTICLES; i++) {
        if (articles[i]) {
            printf("Article %i\n", i);
            printf("Secret: %i\n", articles[i]->secret);
            printf("Length: %i\n", articles[i]->length);
            printf("Note: %s\n", articles[i]->note);
            printf("Signature: %s\n", articles[i]->signature);
            printf("\n");
        }
    }
    for (int i = 0; i < EDITS; i++) {
        if (edits[i]) {
            printf("Edit %i\n", i);
            printf("Article: %i\n", edits[i]->article);
            printf("Type: %i\n", edits[i]->type);
            printf("Offset: %i\n", edits[i]->offset);
            printf("Count: %i\n", edits[i]->count);

            if (edits[i]->type == INSERT) {
                printf("Content: %s\n", edits[i]->content);
            }
            printf("\n");
        }
    }
    puts("===========================");
}
```

After playing around we realise that if we add an article and edit it, the
article is still there. And also we can do nasty stuff with it such as adding
edits etc, and the bound checks somehow are not there.

And also, if we sign this deleted article, the flag will appear.

I do not know why, but I am happy enough to get the flag with the code as
written in `soln.py`.
