$(document).ready(function() {

    // Initialize variables
    var $form = $('#admin-form');
    var $promptInput = $('#prompt-input');
    var $responseInput = $('#response-input');
    var $submitButton = $('#submit-button');
  
    // Submit the form on button click
    $submitButton.click(function(event) {
      event.preventDefault();
      var prompt = $promptInput.val();
      var response = $responseInput.val();
      trainChatbot(prompt, response);
    });
  
    // Function to train the chatbot
    function trainChatbot(prompt, response) {
      $.ajax({
        url: '/train',
        method: 'POST',
        data: {'prompt': prompt, 'response': response},
        success: function(data) {
          alert('Chatbot trained successfully!');
          $promptInput.val('');
          $responseInput.val('');
        },
        error: function(error) {
          alert('Error training chatbot. Please try again later.');
        }
      });
    }
  
  });
  