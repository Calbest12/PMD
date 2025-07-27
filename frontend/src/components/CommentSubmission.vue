<template>
  <div class="comment-section">
    <h3>Comments</h3>

    <form @submit.prevent="submitComment" class="comment-form">
        <textarea v-model="new comment" placeholder="Add a comment..." rows="3"></textarea>
        <button type="submit" :disabled="newComment.trim() ===''">Submit</button>
    </form>

    <div class="comments-history">
      <div v-for="(comment, index) in comments" :key="index" class="comment>
        <p class="meta">
          <strong>{{ comment.user }}</strong> - <span>{{ formatTimestamp(comment.timestamp) }}</span>
        </p>
        <p class="text">{{ comment.text }}</p>
      </div>
    </div>
  </div>
</template>


<script>
export default {
   name: "CommentSection",
   data() {
    return {
     newComment: "",
     comments: [
       {
         user: "Hind",
         text: "Don't forget to update metrics weekly.",
         timestamp: new Date().toISOString()
       },
       {
         user: "Bob",
         text: "I added the API documentation under resources.",
         timestamp: new Date().toISOString()
       }
    ]
  };
},
methods: {
  submitComment() {
    const comment = {
////im going to double check how the current user is stored so this might change still.
      user: this.$store.stat.user.username,
      text: this.newComment,
      timestamp: new Date().toISOString()
    };
    this.comments.unshift(comment);
    this.newComment = "";
  },
  formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
   }
  }
};
</script>


<style scoped>
.comment-section {
    border-top:1px solid #cccccc;
    padding-top: 1rem;
    margin-top: 2rem;
}

.comment-form {
    display: flex;
    flex-direction: column;
    margin-bottom: 1.5rem;
}

.comment-form textarea {
    resize: none;
    padding: 0.5rem;
    margin-button: 0.5rem;
}

.comment-form button {
    align-self: flex-end;
    padding: 0.4rem 1rem;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
}

.comment-form button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

.comments-history {
    border-top: 1px dashed #cccccc;
    padding-top: 1rem;
}

.comment {
    margin-bottom: 1rem;
}

.meta {
    font-size: 0.9rem;
    color: #555555;
}
.text {
    margin: 0.2rem 0 0;
}
</style>